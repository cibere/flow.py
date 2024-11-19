from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Awaitable, Callable

from .jsonrpc import ErrorResponse

if TYPE_CHECKING:
    from .plugin import Plugin
    from .query import Query

LOG = logging.getLogger(__name__)


async def on_error(
    event_method: str, error: Exception, *args: Any, **kwargs: Any
) -> ErrorResponse:
    """gets called when an error occurs in an event"""
    LOG.exception(f"Ignoring exception in event {event_method!r}", exc_info=error)
    return ErrorResponse.internal_error(error)


async def on_action_error(action_name: str, error: Exception) -> ErrorResponse:
    """gets called when an error occurs in an action"""
    LOG.exception(f"Ignoring exception in action ({action_name!r})", exc_info=error)
    return ErrorResponse.internal_error(error)


async def on_query(data: Query):
    raise RuntimeError("'query' should be overridden")


async def on_context_menu(data: list[Any]):
    return []


def get_default_events(plugin: Plugin) -> dict[str, Callable[..., Awaitable[Any]]]:
    return {
        event.__name__: event
        for event in (
            on_error,
            on_query,
            on_context_menu,
            plugin._query_wrapper,
            plugin._initialize_wrapper,
            plugin._context_menu_wrapper,
            on_action_error,
        )
    }
