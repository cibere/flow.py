from __future__ import annotations

import asyncio
import json
import logging
import sys
from asyncio.streams import StreamReader, StreamWriter
from typing import TYPE_CHECKING, Any

from ..errors import PluginExecutionError
from .errors import JsonRPCException
from .objects import JsonRPCError, Option, QueryResponse, Request, Result
from .utils import coro_or_gen

LOG = logging.getLogger(__name__)

if TYPE_CHECKING:
    from ..plugin import Plugin
    from ..settings import Settings

__all__ = ("Client",)


class Client:
    reader: StreamReader
    writer: StreamWriter

    def __init__(self, plugin: Plugin) -> None:
        self.tasks: dict[int, asyncio.Task] = {}
        self.requests: dict[int, asyncio.Future[Result | JsonRPCError]] = {}
        self.request_id = 1
        self.plugin = plugin

    async def request(
        self, method: str, params: list[object] = []
    ) -> Result | JsonRPCError:
        fut: asyncio.Future[Result | JsonRPCError] = asyncio.Future()
        self.request_id += 1
        self.requests[self.request_id] = fut
        msg = Request(method, self.request_id, params).to_message()
        self.writer.write(msg)
        return await fut

    async def __handle_cancellation(self, id: int) -> None:
        if id in self.tasks:
            task = self.tasks.pop(id)
            success = task.cancel()
            if success:
                LOG.info(f"Successfully cancelled task with id {id!r}")
            else:
                LOG.exception(f"Failed to cancel task with id of {id!r}, task={task!r}")
        else:
            LOG.exception(
                f"Failed to cancel task with id of {id!r}, could not find task."
            )

    async def __handle_result(self, result: Result) -> None:
        LOG.debug(f"Result: {result.id}, {result!r}")
        if result.id in self.requests:
            try:
                self.requests.pop(result.id).set_result(result)
            except asyncio.InvalidStateError:
                pass
        else:
            LOG.exception(
                f"Result from unknown request given. ID: {result.id!r}, result={result!r}"
            )

    async def __handle_error(self, id: int, error: JsonRPCError) -> None:
        if id in self.requests:
            self.requests.pop(id).set_exception(Exception(error))
        else:
            LOG.error(f"cancel with no id found: %d", id)

    async def __handle_notification(self, method: str, params: dict[str, Any]) -> None:
        if method == "$/cancelRequest":
            await self.__handle_cancellation(params["id"])
        else:
            LOG.exception(
                f"Unknown notification method received: {method}",
                exc_info=JsonRPCException("Unknown notificaton method received"),
            )

    async def __handle_request(self, request: dict[str, Any]) -> None:
        method = request["method"]
        coro, params = self.plugin._get_coro_from_method(method, request["params"])
        if isinstance(coro, JsonRPCError):
            LOG.exception(
                f"A JsonRPCError error occured while handling request ({request!r}): {coro!r}"
            )
            return await self.write(coro.to_message(id=request["id"]))

        try:
            task = asyncio.create_task(coro_or_gen(coro))
            self.tasks[request["id"]] = task
            try:
                result = await task
            except Exception as e:
                LOG.exception(
                    f"Exception occured while running {f'{self.plugin.__class__.__name__}.{method}'}",
                    exc_info=e,
                )
                return await self.write(
                    JsonRPCError(
                        code=-32603, message="Internal error", data=e
                    ).to_message(id=request["id"])
                )

            if method in ("query", "context_menu"):
                if result is None:
                    e = TypeError("Recieved NoneType instead of list of options")
                    LOG.exception(
                        f"Exception occured while running {f'{self.plugin.__class__.__name__}.{method}'}",
                        exc_info=PluginExecutionError(method, params, e),
                    )
                    return await self.write(
                        JsonRPCError(
                            code=-32603, message="Internal error", data=e
                        ).to_message(id=request["id"])
                    )
                setting_changes = None
                if method == "query":
                    settings: Settings = params[1]
                    setting_changes = settings._changes
                if isinstance(result, QueryResponse):
                    response = result
                elif isinstance(result, Option):
                    response = QueryResponse([result], setting_changes)
                else:
                    response = QueryResponse(result, setting_changes)
                return await self.write(response.to_message(id=request["id"]))
        except json.JSONDecodeError:
            return await self.write(
                JsonRPCError(code=-32700, message="JSON decode error").to_message(
                    id=request["id"]
                )
            )
        except Exception as e:
            LOG.exception(
                f"Unknown error caught while handling request ({request!r})",
                exc_info=e,
            )
            return await self.write(
                JsonRPCError(
                    code=-32603, message="Internal error", data=f"{sys.exc_info()}"
                ).to_message(id=request["id"])
            )

    async def start_listening(self, reader: StreamReader, writer: StreamWriter):
        self.reader = reader
        self.writer = writer

        while 1:
            bytes = await reader.readline()
            line = bytes.decode("utf-8")
            if line == "":
                continue

            LOG.info(f"Received line: {line}")
            message = json.loads(line)

            if "id" not in message:
                LOG.debug(f"Received notification: {message!r}")
                asyncio.create_task(
                    self.__handle_notification(message["method"], message["params"])
                )
            elif "method" in message:
                LOG.debug(f"Received request: {message!r}")
                asyncio.create_task(self.__handle_request(message))
            elif "result" in message:
                LOG.debug(f"Received result: {message!r}")
                asyncio.create_task(self.__handle_result(Result.from_dict(message)))
            elif "error" in message:
                LOG.debug(f"Received error: {message!r}")
                asyncio.create_task(
                    self.__handle_error(
                        message["id"], JsonRPCError.from_dict(message["error"])
                    )
                )
            else:
                LOG.exception(
                    f"Unknown message type received",
                    exc_info=JsonRPCException("Unknown message type received"),
                )

    async def write(self, msg: bytes, drain: bool = True) -> None:
        LOG.debug(f"Sending: {msg!r}")
        self.writer.write(msg)
        if drain:
            await self.writer.drain()
