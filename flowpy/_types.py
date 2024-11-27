from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncIterable, Callable, Coroutine

if TYPE_CHECKING:
    from .query import Query

type SearchHandlerCallbackReturns[T] = Coroutine[Any, Any, T] | AsyncIterable[T]
type SearchHandlerCallback = Callable[[Query], SearchHandlerCallbackReturns]
type SearchHandlerCondition = Callable[[Query], bool]
