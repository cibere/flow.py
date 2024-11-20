from flowpy import Option, Plugin, Query

plugin = Plugin()


@plugin.event
async def on_query(data: Query):
    yield Option(f"Your text is: {data.text}")
    yield Option(f"Your keyword is: {data.keyword}")
    yield Option(f"Your raw text is: {data.raw_text}", sub="keyword + text")


if __name__ == "__main__":
    plugin.run()
