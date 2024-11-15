import json
import logging
from typing import Any

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


class MyPlugin(Plugin):
    async def __call__(self, data: Query):
        result = await self.api.fuzzy_search(data.text, "hello")

        yield Option(
            f"hello: {result.score}",
        )
        yield Option(
            "Show message",
            action=Action(self.api.show_message, "this is a test", "my sub"),
        )


MyPlugin().run()
