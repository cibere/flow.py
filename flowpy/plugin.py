import asyncio
import json
import logging
from typing import Any, AsyncIterable, Awaitable, Iterable

import aioconsole

from .flow_api.client import FlowLauncherAPI, PluginMetadata
from .jsonrpc import ExecuteResponse, JsonRPCClient, Option, QueryResponse
from .query import Query
from .errors import PluginNotInitialized
from .settings import Settings
from .utils import coro_or_gen, setup_logging

LOG = logging.getLogger(__name__)

__all__ = ("Plugin",)

type ReturnOptions = Awaitable[Iterable[Option]] | AsyncIterable[Option]


class Plugin:
    settings: Settings

    def __init__(self) -> None:
        self.jsonrpc: JsonRPCClient = JsonRPCClient(self)
        self.api = FlowLauncherAPI(self.jsonrpc)
        self._metadata: PluginMetadata | None = None
    
    @property
    def metadata(self) -> PluginMetadata:
        """
        Returns the plugin's metadata from `initialize`.

        Raises a `flowpy.PluginNotInitialized` error if plugin hasn't been initialized yet
        """
        if self._metadata:
            return self._metadata
        raise PluginNotInitialized()


    async def query(
        self, raw_data: dict[str, Any], raw_settings: dict[str, Any]
    ) -> QueryResponse:
        data = Query(raw_data)
        self.settings = Settings(raw_settings)
        options = await coro_or_gen(self.__call__(data))
        return QueryResponse(options, self.settings._changes)

    def __call__(self, data: Query) -> ReturnOptions:
        raise RuntimeError("'query' should be overridden")

    async def initialize(self, arg: dict[str, Any]):
        LOG.info(f"Initialize: {json.dumps(arg)}")
        self._metadata = PluginMetadata(arg['currentPluginMetadata'], self.api)
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
