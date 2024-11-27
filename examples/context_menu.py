from flogin import Plugin, Query, Result

plugin = Plugin()


class ContextMenuResult(Result):
    async def context_menu(self):
        yield "This is an example of context menus with flogin"
        yield "flogin is a python library for working with flow"
        yield "flogin was made by cibere"


@plugin.search()
async def on_search(data: Query):
    return ContextMenuResult("I worky")


if __name__ == "__main__":
    plugin.run()
