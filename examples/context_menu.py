from flowpy import Option, Plugin, Query

plugin = Plugin()

@plugin.context_menu
async def my_ctx_menu(options: list[str]):
    return options

@plugin.search()
async def on_search(data: Query):
    return Option("This is a test", context_menu_handler=my_ctx_menu(["test1", "t2", "t3"]))

if __name__ == "__main__":
    plugin.run()