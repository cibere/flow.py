from __future__ import annotations

import asyncio
import json
import logging
import re
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncIterable,
    Awaitable,
    Callable,
    Coroutine,
    Iterable,
    TypeVar,
    TypeVarTuple,
    overload,
)

from .conditions import PlainTextCondition, RegexCondition
from .default_events import get_default_events
from .errors import InvalidContextDataReceived, PluginNotInitialized
from .flow_api.client import FlowLauncherAPI, PluginMetadata
from .jsonrpc import (
    ErrorResponse,
    ExecuteResponse,
    JsonRPCClient,
    QueryResponse,
    Result,
)
from .jsonrpc.responses import BaseResponse
from .query import Query
from .search_handler import SearchHandler
from .settings import Settings
from .utils import MISSING, cached_property, coro_or_gen, setup_logging

if TYPE_CHECKING:
    from ._types import SearchHandlerCallback, SearchHandlerCondition
TS = TypeVarTuple("TS")
EventCallbackT = TypeVar("EventCallbackT", bound=Callable[..., Any])
LOG = logging.getLogger(__name__)

__all__ = ("Plugin",)


class Plugin:
    r"""This class represents your plugin


    Attributes
    --------
    settings: :class:`~flogin.settings.Settings`
        The plugin's settings set by the user
    api: :class:`~flogin.flow_api.client.FlowLauncherAPI`
        An easy way to acess Flow Launcher's API
    """

    def __init__(self) -> None:
        self.jsonrpc: JsonRPCClient = JsonRPCClient(self)
        self.api = FlowLauncherAPI(self.jsonrpc)
        self._metadata: PluginMetadata | None = None
        self._events: dict[str, Callable[..., Awaitable[Any]]] = get_default_events(
            self
        )
        self._search_handlers: list[SearchHandler] = []
        self._results: dict[str, Result] = {}
        self._settings_are_populated: bool = False

    @cached_property
    def settings(self) -> Settings:
        fp = f"../../Settings/Plugins/{self.metadata.name}/Settings.json"
        with open(fp, "r") as f:
            data = json.load(f)
        self._settings_are_populated = True
        LOG.debug(f"Settings filled from file: {data!r}")
        return Settings(data)

    async def _run_event(
        self,
        coro: Callable[..., Awaitable[Any]],
        event_name: str,
        args: Iterable[Any],
        kwargs: dict[str, Any],
        error_handler: Callable[[Exception], Coroutine[Any, Any, Any]] | str = MISSING,
    ) -> Any:
        try:
            return await coro(*args, **kwargs)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            if error_handler is MISSING:
                error_handler = "on_error"
            if isinstance(error_handler, str):
                return await self._events[error_handler](event_name, e, *args, **kwargs)
            else:
                return await error_handler(e)

    def _schedule_event(
        self,
        coro: Callable[..., Awaitable[Any]],
        event_name: str,
        args: Iterable[Any] = MISSING,
        kwargs: dict[str, Any] = MISSING,
        error_handler: Callable[[Exception], Coroutine[Any, Any, Any]] | str = MISSING,
    ) -> asyncio.Task:
        wrapped = self._run_event(
            coro, event_name, args or [], kwargs or {}, error_handler
        )
        return asyncio.create_task(wrapped, name=f"flogin: {event_name}")

    def dispatch(
        self, event: str, *args: Any, **kwargs: Any
    ) -> None | asyncio.Task[None | BaseResponse]:
        method = f"on_{event}"

        # Special Event Cases
        replacements = {
            # "on_context_menu": "_context_menu_wrapper",
            "on_initialize": "_initialize_wrapper",
        }
        method = replacements.get(method, method)

        LOG.debug("Dispatching event %s", method)

        event_callback = self._events.get(method)
        if event_callback:
            return self._schedule_event(event_callback, method, args, kwargs)

    async def _coro_or_gen_to_results(
        self, coro: Awaitable | AsyncIterable
    ) -> list[Result] | ErrorResponse:
        results = []
        raw_results = await coro_or_gen(coro)
        if isinstance(raw_results, ErrorResponse):
            return raw_results
        if isinstance(raw_results, dict):
            res = Result.from_dict(raw_results)
            self._results[res.slug] = res
            results.append(res)
        else:
            if not isinstance(raw_results, list):
                raw_results = [raw_results]
            for raw_res in raw_results:
                res = Result.from_anything(raw_res)
                self._results[res.slug] = res
                results.append(res)
        return results

    async def _initialize_wrapper(self, arg: dict[str, Any]) -> ExecuteResponse:
        LOG.info(f"Initialize: {json.dumps(arg)}")
        self._metadata = PluginMetadata(arg["currentPluginMetadata"], self.api)
        self.dispatch("initialization")
        return ExecuteResponse(hide=False)

    async def process_context_menus(
        self, data: list[Any]
    ) -> QueryResponse | ErrorResponse:
        LOG.debug(f"Context Menu Handler: {data=}")

        if not data:
            raise InvalidContextDataReceived()

        result = self._results.get(data[0])

        if result is not None:
            result.plugin = self
            task = self._schedule_event(
                self._coro_or_gen_to_results,
                event_name=f"ContextMenu-{result.slug}",
                args=[result.context_menu()],
                error_handler=lambda e: self._coro_or_gen_to_results(
                    result.on_context_menu_error(e)
                ),
            )
            results = await task
        else:
            results = []

        if isinstance(results, ErrorResponse):
            return results
        return QueryResponse(results, self.settings._changes)

    async def process_search_handlers(
        self, query: Query
    ) -> QueryResponse | ErrorResponse:
        results = []
        for handler in self._search_handlers:
            if handler.condition(query):
                handler.plugin = self
                task = self._schedule_event(
                    self._coro_or_gen_to_results,
                    event_name=f"SearchHandler-{handler.name}",
                    args=[handler.callback(query)],
                    error_handler=lambda e: self._coro_or_gen_to_results(
                        handler.on_error(query, e)
                    ),
                )
                results = await task
                break

        if isinstance(results, ErrorResponse):
            return results
        return QueryResponse(results, self.settings._changes)

    @property
    def metadata(self) -> PluginMetadata:
        """
        Returns the plugin's metadata.

        Raises
        --------
        :class:`~flogin.errors.PluginNotInitialized`
            This gets raised if the plugin hasn't been initialized yet
        """
        if self._metadata:
            return self._metadata
        raise PluginNotInitialized()

    async def start(self):
        r"""|coro|

        The default startup/setup method. This can be overriden for advanced startup behavior, but make sure to run ``await super().start()`` to actually start your plugin.
        """

        import aioconsole

        reader, writer = await aioconsole.get_standard_streams()
        await self.jsonrpc.start_listening(reader, writer)

    def run(self, *, setup_default_log_handler: bool = True) -> None:
        r"""The default runner. This runs the :func:`~flogin.plugin.Plugin.start` coroutine, and setups up logging.

        Parameters
        --------
        setup_default_log_handler: :class:`bool`
            Whether to setup the default log handler or not, defaults to `True`.
        """

        if setup_default_log_handler:
            setup_logging()

        asyncio.run(self.start())

    def register_search_handler(self, handler: SearchHandler) -> None:
        r"""Register a new search handler

        See the :ref:`search handler section <search_handlers>` for more information about using search handlers.

        Parameters
        -----------
        handler: :class:`~flogin.search_handler.SearchHandler`
            The search handler to be registered
        """

        self._search_handlers.append(handler)
        LOG.info(f"Registered search handler: {handler}")

    def event(self, callback: EventCallbackT) -> EventCallbackT:
        """A decorator that registers an event to listen for.

        All events must be a :ref:`coroutine <coroutine>`.

        .. NOTE::
            See the :ref:`event reference <events>` to see what valid events there are.

        Example
        ---------

        .. code-block:: python3

            @plugin.event
            async def on_initialization():
                print('Ready!')

        """

        name = callback.__name__
        self._events[name] = callback
        return callback

    @overload
    def search(
        self, condition: SearchHandlerCondition
    ) -> Callable[[SearchHandlerCallback], SearchHandler]: ...

    @overload
    def search(
        self, *, text: str
    ) -> Callable[[SearchHandlerCallback], SearchHandler]: ...

    @overload
    def search(
        self, *, pattern: re.Pattern
    ) -> Callable[[SearchHandlerCallback], SearchHandler]: ...

    @overload
    def search(
        self,
    ) -> Callable[[SearchHandlerCallback], SearchHandler]: ...

    def search(
        self,
        condition: SearchHandlerCondition | None = None,
        *,
        text: str = MISSING,
        pattern: re.Pattern = MISSING,
    ) -> Callable[[SearchHandlerCallback], SearchHandler]:
        """A decorator that registers a search handler.

        All search handlers must be a :ref:`coroutine <coroutine>`. See the :ref:`search handler section <search_handlers>` for more information about using search handlers.

        Parameters
        ----------
        condition: Optional[:ref:`condition <condition_example>`]
            The condition to determine which queries this handler should run on. If given, this should be the only argument given.
        text: Optional[:class:`str`]
            A kwarg to quickly add a :class:`~flogin.conditions.PlainTextCondition`. If given, this should be the only argument given.
        pattern: Optional[:class:`re.Pattern`]
            A kwarg to quickly add a :class:`~flogin.conditions.RegexCondition`. If given, this should be the only argument given.

        Example
        ---------

        .. code-block:: python3

            @plugin.on_search()
            async def example_search_handler(data: Query):
                return "This is a result!"

        """

        if condition is None:
            if text is not MISSING:
                condition = PlainTextCondition(text)
            elif pattern is not MISSING:
                condition = RegexCondition(pattern)

        def inner(func: SearchHandlerCallback) -> SearchHandler:
            handler = SearchHandler(condition)
            handler.callback = func  # type: ignore # type is the same
            self.register_search_handler(handler)
            return handler

        return inner
