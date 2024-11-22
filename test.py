from flowpy import Option, Plugin, Query, PlainTextCondition
import re
plugin = Plugin()

@plugin.search(text="cibere")
async def author_easteregg(data: Query):
    return f"That is the name of the person who wrote this plugin"

@plugin.search()
async def on_query(data: Query):
    result = await plugin.api.fuzzy_search(data.text, "Flow")
    return [
        Option(
            f"Flow: {result.score}",
            sub=f"Precision: {result.search_precision}",
            title_highlight_data=result.highlight_data,
        )
    ]

plugin.run()
