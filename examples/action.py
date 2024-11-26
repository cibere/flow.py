from flowpy import ExecuteResponse, Plugin, Query, Result

plugin = Plugin()


class ActionResult(Result):
    async def callback(self):
        await plugin.api.show_notification("flow.py plugin", "I worky!")
        return ExecuteResponse(hide=False)


@plugin.search()
async def on_search(data: Query):
    return ActionResult("I worky")


if __name__ == "__main__":
    plugin.run()
