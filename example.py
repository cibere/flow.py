from flogin import ExecuteResponse, Plugin, Query, Result

my_plugin = Plugin()


class MyResult(Result):
    async def callback(self):
        await my_plugin.api.show_notification(
            "Flogin", "result's callback has been triggered"
        )
        return ExecuteResponse()


@my_plugin.search()
async def blanket(q: Query):
    return MyResult("Blanket Handler Called")


import asyncio

from flogin import Query
from flogin.testing import PluginTester


# Since we use the `show_notification` api method in our result callback, we need to impliment it in our replacement class.
class FakeFlowAPI:
    async def show_notification(self, *args):
        print(f"showing notification with {args!r}")


async def main():
    # Because we don't use the metadata at all, we can just use some bogus data.
    metadata = PluginTester.create_bogus_plugin_metadata()

    # Creating our plugin tester object
    tester = PluginTester(my_plugin, metadata=metadata, flow_api_client=FakeFlowAPI())

    # Creating our query object. In this example, this query would represent a query which was `bambo`, with our plugin's keyword being `bambo`.
    query = Query(
        raw_text="bambo",
        keyword="bambo",
        text="",
    )

    # Testing our search handlers and getting the response
    response = await tester.test_query(query)

    # getting our result
    result = response.results[0]

    # printing out result's title
    print(f"Result title: {result.title}")

    # Executing our result's callback
    await result.callback()


asyncio.run(main())
