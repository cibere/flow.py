Testing your plugin
===================

Writing Tests
--------------
For writing tests, we can use the :class:`~flogin.testing.plugin_tester.PluginTester` class to create tests for our plugin.

:class:`~flogin.testing.plugin_tester.PluginTester` takes 3 arguments:

1. Your plugin

2. `Your plugin's metadata <#your-plugin-metadata>`_

3. `Your FlowLauncherAPI replacement <#your-flowlauncherapi-replacement>`_

*check out the hyperlinked sections for more information on those arguments*

Once you have your tester instance all set up, you can use the :func:`~flogin.testing.plugin_tester.PluginTester.test_query` to test your search handlers.

To test your result's context menu, the :func:`~flogin.testing.plugin_tester.PluginTester.test_context_menu` method has been provided to test your context menus.

to test your result's callbacks, simply call their callbacks manually (:func:`~flogin.jsonrpc.results.Result.callback`).

Example
~~~~~~~
Here is a simple plugin: ::

    from flogin import Plugin, Query, Result, ExecuteResponse

    my_plugin = Plugin()

    class MyResult(Result):
        async def callback(self):
            await my_plugin.api.show_notification("Flogin", "result's callback has been triggered")
            return ExecuteResponse()

    @my_plugin.search()
    async def blanket(q: Query):
        return MyResult("Blanket Handler Called")

And here is a simply testing script for it: ::

    import asyncio

    from flogin.testing import PluginTester
    from flogin import Query

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

Your Plugin metadata
~~~~~~~~~~~~~~~~~~~~
If you pass ``None`` to the ``metadata`` argument, flogin will attempt to retrieve the metadata from your ``plugin.json`` file.

In cases where that is not available or you need to customize your metadata, the :func:`~flogin.testing.plugin_tester.PluginTester.create_bogus_plugin_metadata` and :func:`~flogin.testing.plugin_tester.PluginTester.create_plugin_metadata` methods have been provided.

The :func:`~flogin.testing.plugin_tester.PluginTester.create_plugin_metadata` classmethod provides a cleaner ui for creating a :class:`~flogin.flow_api.plugin_metadata.PluginMetadata` object, with some arguments being optional, and being auto-generated.

The :func:`~flogin.testing.plugin_tester.PluginTester.create_bogus_plugin_metadata` provides a very fast way to generate a "valid" metadata object, by filling it with random data.

Your FlowLauncherAPI replacement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you do not use :class:`~flogin.flow_api.client.FlowLauncherAPI` in the code that you are testing, then the default filler object will do just fine.

However if you use the api at all in the code you want to test, you will want to create a FlowLauncherAPI replacement class for testing and pass it to the ``flow_api_client`` argument in your plugin tester's constructor.

When creating your replacement class, make sure to impliment any and all API methods that you use, and respond accordingly inside of them.

For example, lets say I use the :func:`~flogin.flow_api.client.FlowLauncherAPI.open_settings_menu` method. I would impliment that method into my replacement class, which might look something like this: ::

    class MyFlowAPI:
        async def open_settings_menu(self):
            print("-- Settings menu has been opened --")

That one is pretty easy due to it not returning anything, or doing anything that may affect the plugin. Let's take another example, :func:`~flogin.flow_api.client.FlowLauncherAPI.open_settings_menu`. You can always do something similiar to what we did with :func:`~flogin.flow_api.client.FlowLauncherAPI.open_settings_menu`, however for this example we will handle what will happen if we try to add a keyword to our own plugin. To do this, we will pass our plugin to our api class, and later use that to check the plugin ids, and add the keyword. ::

    class MyFlowAPI:
        def __init__(self, plugin):
            self.plugin = plugin

        async def add_keyword(self, plugin_id: str, keyword: str):
            if plugin_id == self.plugin.metadata.id:
                self.plugin.metadata.keywords.append(keyword)

            print(f"-- Added {keyword!r} keyword to {plugin_id!r} --")
