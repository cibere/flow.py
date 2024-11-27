from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Callable, Coroutine

from .jsonrpc import ErrorResponse

if TYPE_CHECKING:
    from ._types import SearchHandlerCallbackReturns, SearchHandlerCondition
    from .query import Query

LOG = logging.getLogger(__name__)
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

        def on_error(self, error: Exception) -> SearchHandlerCallbackReturns:
            r"""|coro|

            Override this function to add an error response behavior to this handler's callback.

            If the error was handled:
                You can return/yield almost anything, and flow.py will convert it into a list of :class:`~flowpy.jsonrpc.results.Result` objects before sending it to flow.

            If the error was not handled:
                Return a :class:`~flowpy.jsonrpc.responses.ErrorResponse` object

            Parameters
            ----------
            error: :class:`Exception`
                The error that occured

            Returns
            -------
            :class:`~flowpy.jsonrpc.responses.ErrorResponse` | list[:class:`~flowpy.jsonrpc.results.Result`] | :class:`~flowpy.jsonrpc.results.Result` | str | Any
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

        async def on_error(self, error: Exception):
            r"""|coro|

            Override this function to add an error response behavior to this handler's callback.

            If the error was handled:
                You can return/yield almost anything, and flow.py will convert it into a list of :class:`~flowpy.jsonrpc.results.Result` objects before sending it to flow.

            If the error was not handled:
                Return a :class:`~flowpy.jsonrpc.responses.ErrorResponse` object

            Parameters
            ----------
            error: :class:`Exception`
                The error that occured

            Returns
            -------
            :class:`~flowpy.jsonrpc.responses.ErrorResponse` | list[:class:`~flowpy.jsonrpc.results.Result`] | :class:`~flowpy.jsonrpc.results.Result` | str | Any
                A list of results, an results, or something that can be converted into a list of results.

            Yields
            ------
            :class:`~flowpy.jsonrpc.results.Result` | str | Any
                A result object or something that can be converted into a result object.
            """
            LOG.exception(
                f"Ignoring exception in reuslt callback ({self!r})", exc_info=error
            )
            return ErrorResponse.internal_error(error)

    @property
    def name(self) -> str:
        """:class:`str`: The name of the search handler's callback"""
        return self.callback.__name__

    def error[
        T: Callable[[Exception], SearchHandlerCallbackReturns]
    ](self, func: T) -> T:
        """A decorator that registers a error handler for this search handler.

        For more information see :class:`~flowpy.search_handler.SearchHandler.on_error`

        Example
        ---------

        .. code-block:: python3

            @plugin.search()
            async def my_hander(query):
                ..

            @my_handler.error
            async def my_error_handler(error):
                ...

        """

        self.on_error = func  # type: ignore
        return func
