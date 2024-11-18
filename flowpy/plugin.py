import asyncio
import json
import logging
from typing import Any, AsyncIterable, Awaitable, Iterable

import aioconsole

from .errors import PluginNotInitialized
from .flow_api.client import FlowLauncherAPI, PluginMetadata
from .jsonrpc import ExecuteResponse, JsonRPCClient, Option, QueryResponse
from .query import Query
from .settings import Settings
from .utils import coro_or_gen, setup_logging

LOG = logging.getLogger(__name__)

__all__ = ("Plugin",)

type ReturnOptions = Awaitable[Iterable[Option]] | AsyncIterable[Option]


class Plugin:
    r"""This class represents your plugin 


    Attributes
    --------
    settings: :class:`flowpy.settings.Settings`
        The plugin's settings set by the user
    api: :class:`~FlowLauncherAPI`
        An easy way to acess Flow Launcher's API
    """
    settings: Settings

    def __init__(self) -> None:
        self.jsonrpc: JsonRPCClient = JsonRPCClient(self)
        self.api = FlowLauncherAPI(self.jsonrpc)
        self._metadata: PluginMetadata | None = None

    @property
    def metadata(self) -> PluginMetadata:
        """
        :class:`PluginMetadata`: Returns the plugin's metadata from `initialize`.

        Raises
        --------
        :class:`PluginNotInitialized`
            This gets raised if the plugin hasn't been initialized yet, or if the :class:`Plugin.initialize` method was overridden and does not call the original.
        """
        if self._metadata:
            return self._metadata
        raise PluginNotInitialized()

    async def query(
        self, raw_data: dict[str, Any], raw_settings: dict[str, Any]
    ) -> QueryResponse:
        r"""This is a default callback method which handles incoming query requests.

        .. NOTE::
            It is recommended to use the :class:`Plugin.__call__` method instead.
        
        .. WARNING::
            Overridding this will result in the :class:`Plugin.__call__` method, and the :class:`Plugin.settings` attribute to not work.

        Parameters
        --------
        raw_data: dict[:class:`str`, Any]
            The raw query data
        raw_settings: dict[:class:`str`, Any]
            The raw settings
        
        Returns
        --------
        :class:`QueryResponse`
            A query response
        """
        data = Query(raw_data)
        self.settings = Settings(raw_settings)
        options = await coro_or_gen(self.__call__(data))
        return QueryResponse(options, self.settings._changes)

    def __call__(self, data: Query) -> ReturnOptions:
        r"""This is the recommended way to handle query requests
        
        .. NOTE::
            Overriding :class:`Plugin.query` will stop this method from being called.
        
        Parameters
        --------
        data: :class:`Query`
            The query data that was sent with the request
        
        Raises
        --------
        :class:`RuntimeError`
            If this method is not overridden, a :class:`RuntimeError` error will be raised by default.
        
        Returns
        --------
        list[:class:`Option`]
            A list of options to be shown as the result of the query
        
        Yields
        --------
        :class:`Option`
            An option to be added to the result of the query
        """

        raise RuntimeError("'query' should be overridden")

    async def initialize(self, arg: dict[str, Any]) -> ExecuteResponse:
        r"""The response to the initialization request from flow on startup.
        
        .. NOTE::
            Overridding this will cause :class:`Plugin.metadata` to not be filled
        
        .. WARNING::
            If an error happens in this method and an :class:`ExecuteResponse` response is not returned, Flow Launcher will repeatedly silently crash on startup.
        
        Parameters
        --------
        arg: dict[:class:`str`, Any]
            The raw data sent from flow on initialization
        
        Returns
        --------
        :class:`ExecuteResponse`
        """

        LOG.info(f"Initialize: {json.dumps(arg)}")
        self._metadata = PluginMetadata(arg["currentPluginMetadata"], self.api)
        return ExecuteResponse(hide=False)

    async def context_menu(self, data: list[Any]) -> QueryResponse:
        r"""The callback method for context menu requests
        
        .. NOTE::
            Unlike :class:`Plugin.__call__`, you can't just return :class:`Option` objects, you must build the :class:`QueryResponse` response objects yourself.
        
        Parameters
        --------
        data: list[Any]
            The data provided in :class:`Option.context_data` for the option the user wants the context menu for.
        
        Returns
        --------
        :class:`QueryResponse`
        """

        return QueryResponse([])

    def run(self, *, setup_default_log_handler: bool = True) -> None:
        r"""The default runner.
        
        Parameters
        --------
        setup_default_log_handler: :class:`bool`
            Whether to setup the default log handler or not, defaults to `True`.
        """
        
        if setup_default_log_handler:
            setup_logging()

        async def main():
            reader, writer = await aioconsole.get_standard_streams()
            await self.jsonrpc.start_listening(reader, writer)

        asyncio.run(main())
