from flowpy import Action, ExecuteResponse, Option, Plugin, Query

plugin = Plugin()


async def my_action(text: str):
    await plugin.api.show_notification("Test Plugin", f"Your text is: {text}")
    return ExecuteResponse(hide=False)


@plugin.search()
async def on_search(data: Query):
    return Option(
        f"Your text is: {data.text}",
        sub="Click this to initiate the action",
        action=Action(my_action, data.text),
    )


if __name__ == "__main__":
    plugin.run()
