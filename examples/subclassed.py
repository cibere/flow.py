from flowpy import Option, Plugin, Query, subclassed_search


class MyPlugin(Plugin):
    @subclassed_search()
    async def on_query(self, data: Query):
        return [
            f"Your text is: {data.text}",
            f"Your keyword is: {data.keyword}",
            Option(f"Your raw text is: {data.raw_text}", sub="keyword + text"),
        ]


if __name__ == "__main__":
    MyPlugin().run()
