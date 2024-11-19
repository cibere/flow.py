from __future__ import annotations

import asyncio
import json
import logging
from asyncio.streams import StreamReader, StreamWriter
from typing import TYPE_CHECKING, Any, Callable, Coroutine

from .errors import JsonRPCException
from .requests import Request
from .responses import BaseResponse, ErrorResponse
from .result import Result

LOG = logging.getLogger(__name__)

if TYPE_CHECKING:
    from ..plugin import Plugin
    from .option import Action

__all__ = ("JsonRPCClient",)


class JsonRPCClient:
    reader: StreamReader
    writer: StreamWriter

    def __init__(self, plugin: Plugin) -> None:
        self.tasks: dict[int, asyncio.Task] = {}
        self.requests: dict[int, asyncio.Future[Result | ErrorResponse]] = {}
        self._current_request_id = 1
        self.plugin = plugin
        self.action_callback_mapping: dict[
            str, Callable[..., Coroutine[Any, Any, Any]]
        ] = {}

    @property
    def request_id(self) -> int:
        self._current_request_id += 1
        return self._current_request_id

    @request_id.setter
    def request_id(self, value: int) -> None:
        self._current_request_id = value

    async def request(
        self, method: str, params: list[object] = []
    ) -> Result | ErrorResponse:
        fut: asyncio.Future[Result | ErrorResponse] = asyncio.Future()
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

    async def __handle_error(self, id: int, error: ErrorResponse) -> None:
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

        self.request_id = request["id"]

        callback = self.action_callback_mapping.get(method)
        if callback is None:
            task = self.plugin.dispatch(method, *params)
            if not task:
                return
        else:
            task = self.plugin._schedule_event(
                callback,
                method,
                params[0],
                error_handler_event_name="on_action_error",
            )
        self.tasks[request["id"]] = task
        result = await task

        if isinstance(result, BaseResponse):
            result.prepare(self)
            return await self.write(result.to_message(id=request["id"]))
        else:
            return await self.write(
                ErrorResponse.internal_error().to_message(id=request["id"])
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
                        message["id"], ErrorResponse.from_dict(message["error"])
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
