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
    async def __call__(self, data: Query, settings: Settings):
        result = await self.api.fuzzy_search(data.text, "hello")

        yield Option(
            f"hello: {result.score}",
        )
        yield Option("Show message", action=Action(method=self.test))

    async def test(self):
        res = await self.api.show_message("This is a test", "sub")
        LOG.info(res.data)
        return ExecuteResponse(False)


MyPlugin().run()
