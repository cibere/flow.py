import json
from inspect import isasyncgen, iscoroutine
from typing import Any, AsyncIterable, Awaitable


class _MissingSentinel:
    def __bool__(self) -> bool:
        return False

    def __eq__(self, other: Any) -> bool:
        return False


MISSING: Any = _MissingSentinel()

__all__ = ("MISSING", "coro_or_gen")


async def coro_or_gen[T](coro: Awaitable[list[T]] | AsyncIterable[T]) -> list[T] | None:
    if iscoroutine(coro):
        return await coro
    elif isasyncgen(coro):
        return [item async for item in coro]
    else:
        raise RuntimeError(f"Not a coro or gen: {coro!r}")
