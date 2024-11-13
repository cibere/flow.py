import logging
import logging.handlers
from inspect import isasyncgen, iscoroutine
from typing import Any, AsyncIterable, Awaitable, Iterable


class _MissingSentinel:
    def __bool__(self) -> bool:
        return False

    def __eq__(self, other: Any) -> bool:
        return False


MISSING: Any = _MissingSentinel()

LOG = logging.getLogger(__name__)
__all__ = ("setup_logging", "coro_or_gen", "MISSING")


def setup_logging(*, formatter: logging.Formatter | None = None) -> None:
    level = logging.DEBUG

    handler = logging.handlers.RotatingFileHandler(
        "flowpy.log", maxBytes=1000000, encoding="UTF-8"
    )

    if formatter is None:
        dt_fmt = "%Y-%m-%d %H:%M:%S"
        formatter = logging.Formatter(
            "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
        )

    logger = logging.getLogger()
    handler.setFormatter(formatter)
    logger.setLevel(level)
    logger.addHandler(handler)


async def coro_or_gen[T](coro: Awaitable[Iterable[T]] | AsyncIterable[T]) -> list[T]:
    if iscoroutine(coro):
        return await coro
    elif isasyncgen(coro):
        return [item async for item in coro]
    else:
        raise RuntimeError(f"Not a coro or gen: {coro!r}")
