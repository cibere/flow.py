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
__all__ = ("setup_logging", "coro_or_gen", "MISSING", "remove_self_arg_from_func")


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
    """|coro|

    Executes an AsyncIterable or a Coroutine that returns a list of items.

    Parameters
    -----------
    coro: :class:`typing.Awaitable`[:class:`typing.Iterable`] | :class:`typing.AsyncIterable`
        The coroutine or asynciterable to be ran

    Raises
    --------
    TypeError
        Neither a :class:`typing.Coroutine` or an :class:`typing.AsyncIterable` was passed

    Returns
    --------
    List[Any]
        A list of whatever was given from the :class:`typing.Coroutine` or :class:`typing.AsyncIterable`.
    """

    if iscoroutine(coro):
        return await coro
    elif isasyncgen(coro):
        return [item async for item in coro]
    else:
        raise TypeError(f"Not a coro or gen: {coro!r}")

def remove_self_arg_from_func[T](func: T, self) -> T:
    def inner(*args):
        return func(self, *args) # type: ignore
    return inner # type: ignore