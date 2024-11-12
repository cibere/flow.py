import asyncio
import json
import logging
import sys
from typing import TYPE_CHECKING, Any, AsyncIterable, Awaitable, Callable, Iterable

import aioconsole

from .jsonrpc import (
    Action,
    JsonRPCClient,
    ExecuteResponse,
    JsonRPCError,
    Option,
    QueryResponse,
)
from .query import Query
from .settings import Settings
from .utils import coro_or_gen, setup_logging
from .flow_api.client import FlowLauncherAPI

LOG = logging.getLogger(__name__)

__all__ = ("Plugin",)

type ReturnOptions = Awaitable[Iterable[Option]] | AsyncIterable[Option]


class Plugin:
    def __init__(self) -> None:
        self.jsonrpc: JsonRPCClient = JsonRPCClient(self)
        self.api = FlowLauncherAPI(self.jsonrpc)

    async def query(
        self, raw_data: dict[str, Any], raw_settings: dict[str, Any]
    ) -> QueryResponse:
        data = Query(raw_data)
        settings = Settings(raw_settings)
        options = await coro_or_gen(self.__call__(data, settings))
        return QueryResponse(options, settings._changes)

    def __call__(self, data: Query, settings: Settings) -> ReturnOptions:
        raise RuntimeError("'query' should be overridden")

    async def initialize(self, arg: dict[str, Any]):
        LOG.info(f"Initialize: {json.dumps(arg)}")
        return ExecuteResponse(hide=False)

    async def store(self, res):
        LOG.info(f"Store: {json.dumps(res)}")
        return ExecuteResponse(hide=False)

    async def context_menu(self, data: list[Any]) -> QueryResponse:
        return QueryResponse([])

    def run(self, *, setup_default_log_handler: bool = True) -> None:
        if setup_default_log_handler:
            setup_logging()

        async def main():
            reader, writer = await aioconsole.get_standard_streams()
            await self.jsonrpc.start_listening(reader, writer)

        asyncio.run(main())
