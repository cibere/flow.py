from flowpy import Option, Plugin, Query, subclassed_event


class MyPlugin(Plugin):
    @subclassed_event
    async def on_query(self, data: Query):
        return [
            Option(f"Your text is: {data.text}"),
            Option(f"Your keyword is: {data.keyword}"),
            Option(f"Your raw text is: {data.raw_text}", sub="keyword + text"),
        ]


if __name__ == "__main__":
    MyPlugin().run()
