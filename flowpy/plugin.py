import asyncio
import json
import logging
import sys
from typing import TYPE_CHECKING, Any, AsyncIterable, Awaitable, Callable, Iterable

import aioconsole

from .jsonrpc import (
    Action,
    Client,
    ExecuteResponse,
    JsonRPCError,
    Option,
    QueryResponse,
)
from .query import Query
from .settings import Settings
from .utils import setup_logging

LOG = logging.getLogger(__name__)

__all__ = ("Plugin",)

type ReturnOptions = AsyncIterable[Option] | Awaitable[Iterable[Option]] | Awaitable[
    Option
] | Awaitable[QueryResponse]


class Plugin:
    def __init__(self) -> None:
        self.client: Client = Client(self)
        self._additional_method_mapping: dict[str, Callable] = {}

    def _register_action(self, action: Action) -> str:
        name = action.method.__qualname__
        self._additional_method_mapping[name] = action.method
        return name

    def _get_coro_from_method(
        self, method: str, params: list[Any]
    ) -> tuple[Awaitable[list[Any]] | AsyncIterable[Any] | JsonRPCError, list[Any]]:
        LOG.debug(f"{self._additional_method_mapping=!r}")
        if method == "query":
            params = [Query(params[0]), Settings(params[1])]
            func = self.query
        elif method == "context_menu":
            func = self.context_menu
        else:
            func = self._additional_method_mapping.get(method)
            if func is None:
                try:
                    func = getattr(self, method)
                except AttributeError as e:
                    return (
                        JsonRPCError(code=-32601, message="Method not found", data=e),
                        [],
                    )
        try:
            return func(*params), params  # type: ignore
        except TypeError as e:
            return JsonRPCError(code=-32602, message="Invalid params"), []

    async def initialize(self, arg: dict[str, Any]):
        LOG.info(f"Initialize: {json.dumps(arg)}")
        return ExecuteResponse(hide=False)

    async def store(self, res):
        LOG.info(f"Store: {json.dumps(res)}")
        return ExecuteResponse(hide=False)

    def query(self, data: Query, settings: Settings) -> ReturnOptions:
        raise RuntimeError("'query' should be overridden")

    if TYPE_CHECKING:

        def context_menu(self, data: list[Any]) -> ReturnOptions: ...

    else:

        async def context_menu(self, _):
            return []

    def run(self, *, setup_default_log_handler: bool = True) -> None:
        if setup_default_log_handler:
            setup_logging()

        async def main():
            reader, writer = await aioconsole.get_standard_streams()
            await self.client.start_listening(reader, writer)

        asyncio.run(main())
