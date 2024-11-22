from __future__ import annotations

from typing import TYPE_CHECKING

from .jsonrpc.option import Option
from .utils import MISSING, coro_or_gen

if TYPE_CHECKING:
    from ._types import SearchHandlerCallback, SearchHandlerCondition
    from .query import Query

__all__ = ("SearchHandler",)


def _default_condition(q: Query) -> bool:
    return True


class SearchHandler:
    r"""This represents a search handler.
    
    When creating this on your own, the :method:`~flowpy.plugin.Plugin.add_search_handler` method can be used to register it.

    See the `search handler section <search_handlers>` for more information about using search handlers.
    
    There are provided decorators to easily create search handlers: :method:`~flowpy.plugin.Plugin.search` and `subclassed_on_search <subclassed_on_search>`
    
    Attributes
    ----------
    callback: |coroutine|
        The coroutine to be ran as the handler's callback
    condition: `condition <condition_example>`
        A function which is used to determine if this search handler should be used to handle a given query or not
    """

    def __init__(
        self,
        callback: SearchHandlerCallback,
        condition: SearchHandlerCondition | None = None,
    ) -> None:
        if condition is None:
            condition = _default_condition

        self.callback = callback
        self.condition = condition

    async def invoke(self, query: Query) -> list[Option]:
        """|coro|
        
        Executes the handler's callback, evaluates the result, and returns a list of options.

        .. NOTE::
            This bypasses the condition
        """

        coro = self.callback(query)
        raw_options = await coro_or_gen(coro)

        if isinstance(raw_options, dict):
            return [Option.from_dict(raw_options)]
        if not isinstance(raw_options, list):
            raw_options = [raw_options]
        return [Option.from_anything(raw_option) for raw_option in raw_options]

    @property
    def name(self) -> str:
        """:class:`str`: The name of the search handler's callback"""
        return self.callback.__name__
