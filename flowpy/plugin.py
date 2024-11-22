from __future__ import annotations

import asyncio
import inspect
import json
import logging
import re
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncIterable,
    Awaitable,
    Callable,
    Iterable,
    overload,
)

import aioconsole

from .conditions import PlainTextCondition, RegexCondition
from .default_events import get_default_events
from .errors import PluginNotInitialized
from .flow_api.client import FlowLauncherAPI, PluginMetadata
from .jsonrpc import ExecuteResponse, JsonRPCClient, Option, QueryResponse
from .jsonrpc.responses import BaseResponse
from .query import Query
from .search_handler import SearchHandler
from .settings import Settings
from .utils import MISSING, coro_or_gen, remove_self_arg_from_func, setup_logging

if TYPE_CHECKING:
    from ._types import (
        SearchHandlerCallback,
        SearchHandlerCallbackInClass,
        SearchHandlerCondition,
    )

LOG = logging.getLogger(__name__)

__all__ = ("Plugin", "subclassed_event", "subclassed_search")


class Plugin:
    r"""This class represents your plugin


    Attributes
    --------
    settings: :class:`~flowpy.settings.Settings`
        The plugin's settings set by the user
    api: :class:`~flowpy.flow_api.client.FlowLauncherAPI`
        An easy way to acess Flow Launcher's API
    """

    def __init__(self) -> None:
        self.settings = Settings({})
        self.jsonrpc: JsonRPCClient = JsonRPCClient(self)
        self.api = FlowLauncherAPI(self.jsonrpc)
        self._metadata: PluginMetadata | None = None
        self._events: dict[str, Callable[..., Awaitable[Any]]] = get_default_events(
            self
        )
        self._search_handlers: list[SearchHandler] = []

        for base in reversed(self.__class__.__mro__):
            for elem, value in base.__dict__.items():
                try:
                    getattr(value, "__flowpy_is_event__")
                except AttributeError:
                    pass
                else:
                    self._events[elem] = remove_self_arg_from_func(value, self)

                if isinstance(value, SearchHandler):
                    self._search_handlers.append(value)
                    value.parent = self

    async def _run_event(
        self,
        coro: Callable[..., Awaitable[Any]],
        event_name: str,
        args: Iterable[Any],
        kwargs: dict[str, Any],
        error_handler_event_name: str = MISSING,
    ) -> Any:
        try:
            return await coro(*args, **kwargs)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            return await self._events[error_handler_event_name or "on_error"](
                event_name, e, *args, **kwargs
            )

    def _schedule_event(
        self,
        coro: Callable[..., Awaitable[Any]],
        event_name: str,
        args: Iterable[Any] = MISSING,
        kwargs: dict[str, Any] = MISSING,
        error_handler_event_name: str = MISSING,
    ) -> asyncio.Task:
        wrapped = self._run_event(
            coro, event_name, args or [], kwargs or {}, error_handler_event_name
        )
        return asyncio.create_task(wrapped, name=f"flow.py: {event_name}")

    def dispatch(
        self, event: str, *args: Any, **kwargs: Any
    ) -> None | asyncio.Task[None | BaseResponse]:
        method = f"on_{event}"

        # Special Event Cases
        replacements = {
            "on_context_menu": "_context_menu_wrapper",
            "on_initialize": "_initialize_wrapper",
        }
        method = replacements.get(method, method)

        LOG.debug("Dispatching event %s", method)

        event_callback = self._events.get(method)
        if event_callback:
            return self._schedule_event(event_callback, method, args, kwargs)

    async def _coro_or_gen_to_options(
        self, coro: Awaitable | AsyncIterable
    ) -> AsyncIterable[Option]:
        raw_options = await coro_or_gen(coro)
        if isinstance(raw_options, dict):
            yield Option.from_dict(raw_options)
            raise StopAsyncIteration
        if not isinstance(raw_options, list):
            raw_options = [raw_options]
        for raw_option in raw_options:
            yield Option.from_anything(raw_option)

    async def _context_menu_wrapper(self, context_data: list[Any]) -> QueryResponse:
        callback = self._events["on_context_menu"]

        options = [
            opt async for opt in self._coro_or_gen_to_options(callback(context_data))
        ]
        return QueryResponse(options, self.settings._changes)

    async def _initialize_wrapper(self, arg: dict[str, Any]) -> ExecuteResponse:
        LOG.info(f"Initialize: {json.dumps(arg)}")
        self._metadata = PluginMetadata(arg["currentPluginMetadata"], self.api)
        self.dispatch("initialization")
        return ExecuteResponse(hide=False)

    async def process_search_handlers(self, query: Query) -> QueryResponse:
        r"""|coro|

        Runs and processes the registered search handlers.
        See the :ref:`search handler section <search_handlers>` for more information about using search handlers.

        Parameters
        ----------
        query: :class:`~flowpy.query.Query`
            The query object to be give to the search handlers
        """

        options = []
        for handler in self._search_handlers:
            if handler.condition(query):
                task = self._schedule_event(
                    handler.invoke,
                    event_name=f"SearchHandler-{handler.name}",
                    args=[query],
                    error_handler_event_name="on_search_error",
                )
                options = await task
                break

        return QueryResponse(options, self.settings._changes)

    @property
    def metadata(self) -> PluginMetadata:
        """
        Returns the plugin's metadata.

        Raises
        --------
        :class:`~flowpy.errors.PluginNotInitialized`
            This gets raised if the plugin hasn't been initialized yet
        """
        if self._metadata:
            return self._metadata
        raise PluginNotInitialized()

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

    def register_search_handler(self, handler: SearchHandler) -> None:
        r"""Register a new search handler

        See the :ref:`search handler section <search_handlers>` for more information about using search handlers.

        Parameters
        -----------
        handler: :class:`~flowpy.search_handler.SearchHandler`
            The search handler to be registered
        """

        self._search_handlers.append(handler)

    def event[T: Callable[..., Any]](self, callback: T) -> T:
        """A decorator that registers an event to listen for.

        Aside from the :ref:`on_query <on_query>` and :ref:`on_context_menu <on_context_menu>` events, all events must be a :ref:`coroutine <coroutine>`.

        .. NOTE::
            See the :ref:`event reference <events>` to see what valid events there are.

        .. NOTE::
            This is to be used outside of a :class:`Plugin` subclass, use :ref:`subclassed_event <subclassed_event>` if it will be used inside of a subclass.

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

        .. NOTE::
            This is to be used outside of a :class:`Plugin` subclass, use :ref:`subclassed_search <subclassed_search>` if it will be used inside of a subclass.

        Parameters
        ----------
        condition: Optional[:ref:`condition <condition_example>`]
            The condition to determine which queries this handler should run on. If given, this should be the only argument given.
        text: Optional[:class:`str`]
            A kwarg to quickly add a :class:`~flowpy.conditions.PlainTextCondition`. If given, this should be the only argument given.
        pattern: Optional[:class:`re.Pattern`]
            A kwarg to quickly add a :class:`~flowpy.conditions.RegexCondition`. If given, this should be the only argument given.

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
            handler = SearchHandler(func, condition)
            self.register_search_handler(handler)
            return handler

        return inner


def subclassed_event[T: Callable[..., Any]](func: T) -> T:
    """A decorator that registers an event to listen for.

    Aside from the `query` and `context_menu` events, all events must be a :ref:`coroutine <coroutine>`.

    .. NOTE::
        See the :ref:`event reference <events>` to see what valid events there are.

    .. NOTE::
        This is to be used within a :class:`Plugin` subclass, use :method:`Plugin.event` if it will be used outside of a subclass.

    Example
        ---------

        .. code-block:: python3

            class MyPlugin(Plugin):
                @subclassed_event
                async def on_initialization(self):
                    print('Ready!')
    """

    setattr(func, "__flowpy_is_event__", True)
    return func


@overload
def subclassed_search(
    condition: SearchHandlerCondition,
) -> Callable[[SearchHandlerCallbackInClass], SearchHandler]: ...


@overload
def subclassed_search(
    *, text: str
) -> Callable[[SearchHandlerCallbackInClass], SearchHandler]: ...


@overload
def subclassed_search(
    *, pattern: re.Pattern
) -> Callable[[SearchHandlerCallbackInClass], SearchHandler]: ...


@overload
def subclassed_search() -> Callable[[SearchHandlerCallbackInClass], SearchHandler]: ...


def subclassed_search(
    condition: SearchHandlerCondition | None = None,
    *,
    text: str = MISSING,
    pattern: re.Pattern = MISSING,
) -> Callable[[SearchHandlerCallbackInClass], SearchHandler]:
    """A decorator that registers a search handler.

    All search handlers must be a :ref:`coroutine <coroutine>`. See the :ref:`search handler section <search_handlers>` for more information about using search handlers.

    .. NOTE::
        This is to be used outside of a :class:`Plugin` subclass, use :ref:`subclassed_search <subclassed_search>` if it will be used inside of a subclass.

    Parameters
    ----------
    condition: Optional[:ref:`condition <condition_example>`]
        The condition to determine which queries this handler should run on. If given, this should be the only argument given.
    text: Optional[:class:`str`]
        A kwarg to quickly add a :class:`~flowpy.conditions.PlainTextCondition`. If given, this should be the only argument given.
    pattern: Optional[:class:`re.Pattern`]
        A kwarg to quickly add a :class:`~flowpy.conditions.RegexCondition`. If given, this should be the only argument given.

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
        handler = SearchHandler(func, condition)
        return handler

    return inner  # type: ignore
