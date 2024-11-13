from __future__ import annotations

import asyncio
import json
import logging
import sys
from asyncio.streams import StreamReader, StreamWriter
from typing import TYPE_CHECKING, Any, Callable

from ..errors import PluginExecutionError
from .base_object import ToMessageBase as BaseResponse
from .errors import JsonRPCException
from .option import Action
from .requests import Request
from .responses import JsonRPCError, QueryResponse
from .result import Result

LOG = logging.getLogger(__name__)

if TYPE_CHECKING:
    from ..plugin import Plugin

__all__ = ("JsonRPCClient",)


class JsonRPCClient:
    reader: StreamReader
    writer: StreamWriter

    def __init__(self, plugin: Plugin) -> None:
        self.tasks: dict[int, asyncio.Task] = {}
        self.requests: dict[int, asyncio.Future[Result | JsonRPCError]] = {}
        self._current_request_id = 1
        self.plugin = plugin
        self.method_mappings: dict[str, Callable] = {}

    @property
    def request_id(self) -> int:
        self._current_request_id += 1
        return self._current_request_id

    async def request(
        self, method: str, params: list[object] = []
    ) -> Result | JsonRPCError:
        fut: asyncio.Future[Result | JsonRPCError] = asyncio.Future()
        rid = self.request_id
        self.requests[rid] = fut
        msg = Request(method, rid, params).to_message(rid)
        await self.write(msg, drain=False)
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
        params = request["params"]
        func = self.method_mappings.get(method)
        if func is None:
            try:
                func = getattr(self.plugin, method)
            except AttributeError as e:
                return await self.write(
                    JsonRPCError(
                        code=-32601, message="Method not found", data=e
                    ).to_message(request["id"])
                )
        else:
            if params:
                params = params[0]
        try:
            coro = func(*params)
        except TypeError as e:
            LOG.exception(
                f"Ran into a TypeError while getting the coro of the {method!r} method, returning invalid params error. Params: {params!r}",
                exc_info=e,
            )
            return await self.write(
                JsonRPCError(code=-32602, message="Invalid params").to_message(
                    id=request["id"]
                )
            )

        try:
            task = asyncio.create_task(coro)
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

            if isinstance(result, BaseResponse):
                if isinstance(result, QueryResponse):
                    [
                        self.register_action(opt.action)
                        for opt in result.options
                        if opt.action
                    ]
                return await self.write(result.to_message(id=request["id"]))
            else:
                e = PluginExecutionError(
                    method,
                    params,
                    TypeError(
                        f"Return type of method was not of Response. Returned: {result!r}"
                    ),
                )
                return await self.write(
                    JsonRPCError(
                        code=-32603, message="Internal error", data=e
                    ).to_message(id=request["id"])
                )
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
                LOG.exception(f"Received error: {message!r}")
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

    def register_action(self, action: Action) -> str:
        name = action.method.__qualname__
        self.method_mappings[name] = action.method
        action.id = self.request_id
        return name
