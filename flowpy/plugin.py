import asyncio
import inspect
import json
import logging
from typing import Any, Awaitable, Callable, Concatenate, Iterable, TypeVar

import aioconsole

from .default_events import get_default_events
from .errors import PluginNotInitialized
from .flow_api.client import FlowLauncherAPI, PluginMetadata
from .jsonrpc import ExecuteResponse, JsonRPCClient, QueryResponse
from .jsonrpc.responses import BaseResponse
from .query import Query
from .settings import Settings
from .utils import MISSING, coro_or_gen, setup_logging

LOG = logging.getLogger(__name__)

__all__ = ("Plugin", "subclassed_event")


class Plugin:
    r"""This class represents your plugin


    Attributes
    --------
    settings: :class:`Settings`
        The plugin's settings set by the user
    api: :class:`FlowLauncherAPI`
        An easy way to acess Flow Launcher's API
    """

    settings: Settings

    def __init__(self) -> None:
        self.jsonrpc: JsonRPCClient = JsonRPCClient(self)
        self.api = FlowLauncherAPI(self.jsonrpc)
        self._metadata: PluginMetadata | None = None
        self._events: dict[str, Callable[..., Awaitable[Any]]] = get_default_events(
            self
        )

        for base in reversed(self.__class__.__mro__):
            for elem, value in base.__dict__.items():
                try:
                    getattr(value, "__flowpy_is_event__")
                except AttributeError:
                    continue
                else:

                    def foo(*args):
                        LOG.debug("Running subclassed event")
                        LOG.debug(f"{elem=}")
                        LOG.debug(f"{value=}")
                        LOG.debug(f"{args=}")
                        LOG.debug(f"{self._events=}")
                        return value(self, *args)

                    self._events[elem] = value  # lambda *args: value(self, *args)
        # self._events.update({name:func for name, func in inspect.getmembers(self, lambda x: getattr(x, "__flowpy_is_event__", False))})

    async def _run_event(
        self,
        coro: Callable[..., Awaitable[BaseResponse | None]],
        event_name: str,
        args: Iterable[Any],
        kwargs: dict[str, Any],
        error_handler_event_name: str = MISSING,
    ) -> BaseResponse | None:
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
        coro: Callable[..., Awaitable[BaseResponse | None]],
        event_name: str,
        args: Iterable[Any] = MISSING,
        kwargs: dict[str, Any] = MISSING,
        error_handler_event_name: str = MISSING,
    ) -> asyncio.Task[BaseResponse | None]:
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
            "on_query": "_query_wrapper",
            "on_context_menu": "_context_menu_wrapper",
            "on_initialize": "_initialize_wrapper",
        }
        method = replacements.get(method, method)

        LOG.debug("Dispatching event %s", method)

        event_callback = self._events.get(method)
        if event_callback:
            return self._schedule_event(event_callback, method, args, kwargs)

    async def _query_wrapper(
        self, raw_query: dict[str, Any], raw_settings: dict[str, Any]
    ) -> QueryResponse:
        callback = self._events["on_query"]
        data = Query(raw_query)
        self.settings = Settings(raw_settings)

        options = await coro_or_gen(callback(data))
        return QueryResponse(options, self.settings._changes)

    async def _context_menu_wrapper(self, context_data: list[Any]) -> QueryResponse:
        callback = self._events["on_context_menu"]
        options = await coro_or_gen(callback(context_data))
        return QueryResponse(options, self.settings._changes)

    async def _initialize_wrapper(self, arg: dict[str, Any]) -> ExecuteResponse:
        LOG.info(f"Initialize: {json.dumps(arg)}")
        self._metadata = PluginMetadata(arg["currentPluginMetadata"], self.api)
        self.dispatch("initialization")
        return ExecuteResponse(hide=False)

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

    def event[T: Callable[..., Any]](self, callback: T) -> T:
        """A decorator that registers an event to listen for.

        Aside from the `query` and `context_menu` events, all events must be a :ref:`coroutine <coroutine>`.

        .. NOTE::
            See the :ref:`event reference <events>` to see what valid events there are.

        .. NOTE::
            This is to be used outside of a :class:`Plugin` subclass, use :func:`subclassed_event` if it will be used inside of a subclass.

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
