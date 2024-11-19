import inspect
import logging
from typing import Any, Awaitable, Callable, TypeVarTuple

from flowpy import Action, ExecuteResponse, Option, Plugin, Query, QueryResponse
from flowpy.plugin import subclassed_event

LOG = logging.getLogger(__name__)
TS = TypeVarTuple("TS")


class MyPlugin(Plugin):
    @subclassed_event
    async def on_query(self, query: Query):
        yield Option(f"Hi: {query.text}")


MyPlugin().run()
