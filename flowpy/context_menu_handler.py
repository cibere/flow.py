from __future__ import annotations

from typing import Any, Callable
import random
from .jsonrpc.option import Option
from .utils import MISSING, coro_or_gen


__all__ = ("ContextMenuHandler",)

class ContextMenuHandler:
    r"""This represents a context menu handler.

    There is a provided decorator to easily create context menu handlers: :func:`~flowpy.plugin.Plugin.context_menu`

    See the :ref:`context menu handler section <ctx_menu_handlers>` for more information about using context menu handlers.

    Attributes
    ------------
    callback: :ref:`coroutine <coroutine>`
        The :ref:`coroutine <coroutine>` to be ran as the handler's callback
    args: Iterable[Any]
        The positional arguments that should be passed to the callback
    kwargs: dict[str, Any]
        The keyword arguments that should be passed to the callback
    """

    def __init__[**P](
        self,
        callback: Callable[P, Any],
        *args: P.args,
        **kwargs: P.kwargs
    ) -> None:
        self.callback = callback
        self.__args = args
        self.__kwargs = kwargs
        self.slug = "".join(random.choices("QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890", k=15))

    async def invoke(self) -> list[Option]:
        """|coro|

        Executes the handler's callback, evaluates the result, and returns a list of options.

        Returns
        --------
        list[:class:`~flowpy.jsonrpc.option.Option`]
        """

        coro = self.callback(*self.__args, **self.__kwargs)
        raw_options = await coro_or_gen(coro)

        if isinstance(raw_options, dict):
            return [Option.from_dict(raw_options)]
        if not isinstance(raw_options, list):
            raw_options = [raw_options]
        return [Option.from_anything(raw_option) for raw_option in raw_options]

    @property
    def name(self) -> str:
        """:class:`str`: The name of the handler's callback"""
        return self.callback.__name__

    def __repr__(self) -> str:
        return f"<ContextMenuHandler name={self.name!r}, slug={self.slug!r}, callback={self.callback!r}, args={self.__args!r}, kwargs={self.__kwargs!r}"