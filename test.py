import inspect
import json
import logging
from typing import Any, Awaitable, Callable, TypeVarTuple

from flowpy import (
    Action,
    ExecuteResponse,
    Option,
    Plugin,
    Query,
    Result,
    SettingNotFound,
    Settings,
)

LOG = logging.getLogger(__name__)
TS = TypeVarTuple("TS")


class MyPlugin(Plugin):
    async def __call__(self, data: Query):
        result = await self.api.fuzzy_search(data.text, "hello")

        yield Option(
            f"hello: {result.score}",
        )

        def gen(method: Callable[[*TS], Awaitable[Any]], *args: *TS):
            return Option(method.__qualname__, action=Action(method, *args))

        for name, val in inspect.getmembers(self.api):
            if (
                getattr(val, "__func__", None) is not None
                and getattr(val, "__self__", None) is not None
            ):
                yield gen(val)


MyPlugin().run()
