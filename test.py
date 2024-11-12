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
        yield Option("Click to test1", action=Action(100, self.api.open_settings_menu, hide_after_finish=True))
        yield Option("Click to test2", action=Action(100, self.api.open_settings_menu, hide_after_finish=False))

MyPlugin().run()
