from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncIterable, Callable, Coroutine

if TYPE_CHECKING:
    from .query import Query
else:
    Query = Any

SearchHandlerCallbackReturns = Coroutine[Any, Any, Any] | AsyncIterable[Any]
SearchHandlerCallback = Callable[[Query], SearchHandlerCallbackReturns]
SearchHandlerCondition = Callable[[Query], bool]
RawSettings = dict[str, Any]
