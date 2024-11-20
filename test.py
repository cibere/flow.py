from flowpy import Option, Plugin, Query, ExecuteResponse, Action
import logging

log = logging.getLogger("Test Plugin")
plugin = Plugin()

async def my_action(text: str):
    await plugin.api.show_notification("Test Plugin", F"Your text is: {text}")
    return ExecuteResponse(hide=False)

@plugin.event
async def on_query(data: Query):
    yield Option(f"Your text is: {data.text}", sub="Click this to initiate the action", action=Action(my_action, data.text))

@plugin.event
async def on_initialization():
    log.info("Plugin has been initialized")

if __name__ == "__main__":
    plugin.run()
