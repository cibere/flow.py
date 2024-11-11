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
    async def query(self, data: Query, settings: Settings):
        result = await self.client.request("FuzzySearch", [data.text, "hello"])
        assert isinstance(result, Result)
        LOG.debug(result)

        yield Option(
            f"hello: {result.result['score']}",
            title_highlight_data=result.result.get("matchData", list()),
            action=Action(id=0, method=self.store, parameters=(result.result,)),
        )
        yield Option(
            "Click here to try hide=true",
            action=Action(id=0, method=self.test, parameters=(True,)),
        )
        yield Option(
            "Click here to try hide=false",
            action=Action(id=1, method=self.test, parameters=(False,)),
        )

    async def test(self, hide: bool):
        return ExecuteResponse(hide)


MyPlugin().run()
