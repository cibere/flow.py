from flowpy import Plugin, Query, Settings, Option

class ReturnListPlugin(Plugin):
    async def __call__(self, data: Query, settings: Settings):
        return [
            Option(f"Your text is: {data.text}"),
            Option(f"Your keyword is: {data.keyword}"),
            Option(f"Your raw text is: {data.raw_text}", sub="keyword + text")
        ]

if __name__ == "__main__":
    ReturnListPlugin().run()