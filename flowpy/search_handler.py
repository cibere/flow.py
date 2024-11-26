from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ._types import SearchHandlerCallback, SearchHandlerCondition, SearchHandlerCallbackReturns
    from .query import Query

__all__ = ("SearchHandler",)


def _default_condition(q: Query) -> bool:
    return True


class SearchHandler:
    r"""This represents a search handler.

    When creating this on your own, the :func:`~flowpy.plugin.Plugin.register_search_handler` method can be used to register it.

    See the :ref:`search handler section <search_handlers>` for more information about using search handlers.

    There is a provided decorator to easily create search handlers: :func:`~flowpy.plugin.Plugin.search`

    Attributes
    ------------
    condition: :ref:`condition <condition_example>`
        A function which is used to determine if this search handler should be used to handle a given query or not
    """

    def __init__(
        self,
        condition: SearchHandlerCondition | None = None,
    ) -> None:
        if condition is None:
            condition = _default_condition

        self.condition = condition
    
    if TYPE_CHECKING:
        def callback(self, query: Query) -> SearchHandlerCallbackReturns:
            r"""|coro|

            Override this function to add the search handler behavior you want for the set condition.

            This method can return/yield almost anything, and flow.py will convert it into a list of :class:`~flowpy.jsonrpc.results.Result` objects before sending it to flow.

            Returns
            -------
            list[:class:`~flowpy.jsonrpc.results.Result`] | :class:`~flowpy.jsonrpc.results.Result` | str | Any
                A list of results, an results, or something that can be converted into a list of results.

            Yields
            ------
            :class:`~flowpy.jsonrpc.results.Result` | str | Any
                A result object or something that can be converted into a result object.
            """
            ...
    else:
        async def callback(self, query: Query):
            r"""|coro|

            Override this function to add the search handler behavior you want for the set condition.

            This method can return/yield almost anything, and flow.py will convert it into a list of :class:`~flowpy.jsonrpc.results.Result` objects before sending it to flow.

            Returns
            -------
            list[:class:`~flowpy.jsonrpc.results.Result`] | :class:`~flowpy.jsonrpc.results.Result` | str | Any
                A list of results, an results, or something that can be converted into a list of results.

            Yields
            ------
            :class:`~flowpy.jsonrpc.results.Result` | str | Any
                A result object or something that can be converted into a result object.
            """
            raise RuntimeError("Callback was not overriden")


    @property
    def name(self) -> str:
        """:class:`str`: The name of the search handler's callback"""
        return self.callback.__name__
