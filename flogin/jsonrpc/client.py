from __future__ import annotations

import asyncio
import json
import logging
from asyncio.streams import StreamReader, StreamWriter
from typing import TYPE_CHECKING, Any

from .errors import JsonRPCException
from .requests import Request
from .responses import BaseResponse, ErrorResponse

LOG = logging.getLogger(__name__)

if TYPE_CHECKING:
    from ..plugin import Plugin

__all__ = ("JsonRPCClient",)


class JsonRPCClient:
    reader: StreamReader
    writer: StreamWriter

    def __init__(self, plugin: Plugin) -> None:
        self.tasks: dict[int, asyncio.Task] = {}
        self.requests: dict[int, asyncio.Future[Any | ErrorResponse]] = {}
        self._current_request_id = 1
        self.plugin = plugin

    @property
    def request_id(self) -> int:
        self._current_request_id += 1
        return self._current_request_id

    @request_id.setter
    def request_id(self, value: int) -> None:
        self._current_request_id = value

    async def request(
        self, method: str, params: list[object] = []
    ) -> Any | ErrorResponse:
        fut: asyncio.Future[Any | ErrorResponse] = asyncio.Future()
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

    async def __handle_result(self, result: dict) -> None:
        rid = result["id"]

        LOG.debug(f"Result: {rid}, {result!r}")
        if rid in self.requests:
            try:
                self.requests.pop(rid).set_result(result)
            except asyncio.InvalidStateError:
                pass
        else:
            LOG.exception(
                f"Result from unknown request given. ID: {rid!r}, result={result!r}"
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
        method: str = request["method"]
        params: list[Any] = request["params"]
        task = None
        error_handler = "on_error"

        self.request_id = request["id"]

        if method.startswith("flogin.action"):
            slug = method.removeprefix("flogin.action.")
            result = self.plugin._results.get(slug)
            if result:
                callback = result.callback
                error_handler = result.on_error
                result.plugin = self.plugin
                task = self.plugin._schedule_event(
                    callback, method, error_handler=error_handler
                )

        if task is None:
            task = self.plugin.dispatch(method, *params)
            if not task:
                return

        self.tasks[request["id"]] = task
        result = await task

        if isinstance(result, BaseResponse):
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
                asyncio.create_task(self.__handle_result(message))
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
