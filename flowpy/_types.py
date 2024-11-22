from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncIterable, Callable, Coroutine

if TYPE_CHECKING:
    from .query import Query

type SearchHandlerCallbackReturns = Coroutine[Any, Any, Any] | AsyncIterable[Any]
type SearchHandlerCallback = Callable[[Query], SearchHandlerCallbackReturns]
type SearchHandlerCallbackInClass[T] = Callable[
    [T, Query], SearchHandlerCallbackReturns
]
type SearchHandlerCondition = Callable[[Query], bool]
