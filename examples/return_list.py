from flowpy import Option, Plugin, Query

plugin = Plugin()


@plugin.search()
async def on_search(data: Query):
    return [
        f"Your text is: {data.text}",
        f"Your keyword is: {data.keyword}",
        Option(f"Your raw text is: {data.raw_text}", sub="keyword + text"),
    ]


if __name__ == "__main__":
    plugin.run()
