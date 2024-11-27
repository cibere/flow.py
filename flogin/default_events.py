from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Awaitable, Callable

from .jsonrpc import ErrorResponse
from .query import Query
from .settings import Settings

if TYPE_CHECKING:
    from .plugin import Plugin


LOG = logging.getLogger(__name__)

__all__ = ("on_error",)


async def on_error(
    event_method: str, error: Exception, *args: Any, **kwargs: Any
) -> ErrorResponse:
    """gets called when an error occurs in an event"""
    LOG.exception(f"Ignoring exception in event {event_method!r}", exc_info=error)
    return ErrorResponse.internal_error(error)


def get_default_events(plugin: Plugin) -> dict[str, Callable[..., Awaitable[Any]]]:
    def on_query(data: dict[str, Any], raw_settings: dict[str, Any]):
        query = Query(data)
        if plugin._settings_are_populated is False:
            plugin.settings = Settings(raw_settings)
        else:
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
            plugin._initialize_wrapper,
        )
    }
