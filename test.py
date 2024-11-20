from flowpy import Option, Plugin, Query

plugin = Plugin()


@plugin.event
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
