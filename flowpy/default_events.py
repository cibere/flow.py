from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Awaitable, Callable

from .jsonrpc import ErrorResponse
from .query import Query

if TYPE_CHECKING:
    from .plugin import Plugin


LOG = logging.getLogger(__name__)

__all__ = (
    "on_error",
    "on_action_error",
    "on_context_menu",
    "on_search_error",
    "on_context_menu_error",
)


async def on_error(
    event_method: str, error: Exception, *args: Any, **kwargs: Any
) -> ErrorResponse:
    """gets called when an error occurs in an event"""
    LOG.exception(f"Ignoring exception in event {event_method!r}", exc_info=error)
    return ErrorResponse.internal_error(error)


async def on_action_error(
    action_name: str, error: Exception, *args, **kwargs
) -> ErrorResponse:
    """gets called when an error occurs in an action"""
    LOG.exception(f"Ignoring exception in action ({action_name!r})", exc_info=error)
    return ErrorResponse.internal_error(error)


async def on_context_menu(data: list[Any]):
    return []


async def on_search_error(
    handler_name: str, error: Exception, query: Query
) -> ErrorResponse:
    """gets called when an error occurs in a search handler"""
    LOG.exception(f"Ignoring exception in action ({handler_name!r})", exc_info=error)
    return ErrorResponse.internal_error(error)


async def on_context_menu_error(
    handler_name: str, error: Exception, *args, **kwargs
) -> ErrorResponse:
    """gets called when an error occurs in a context menu handler"""
    LOG.exception(
        f"Ignoring exception in context menu handler ({handler_name!r})", exc_info=error
    )
    return ErrorResponse.internal_error(error)


def get_default_events(plugin: Plugin) -> dict[str, Callable[..., Awaitable[Any]]]:
    def on_query(data: dict[str, Any], raw_settings: dict[str, Any]):
        query = Query(data)
        plugin.settings._update(raw_settings)
        return plugin.process_search_handlers(query)

    def on_context_menu(data: list[str]):
        return plugin.process_context_menus(data)

    return {
        event.__name__: event
        for event in (
            on_error,
            on_query,
            on_context_menu,
            on_search_error,
            plugin._initialize_wrapper,
            on_action_error,
            on_context_menu_error,
        )
    }
