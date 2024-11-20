:orphan:

.. currentmodule:: flowpy

.. _quickstart:

Quickstart
============

This page gives a brief introduction to the library. It assumes you have the library installed,
if you don't check the :ref:`installing` portion.

.. NOTE::
    To get yourself familiar with flow, check out their `guide <https://www.flowlauncher.com/docs/#/py-develop-plugins?id=about-flow39s-python-plugins>`_ for creating a plugin with the V1 API

A Minimal Plugin
---------------

Let's make a plugin which compares how similar the user's query is with the word ``Flow``.

.. code-block:: python3
    :linenos:

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


There's a lot going on here, so let's walk you through it line by line.

1. The first line just imports the library, if this raises a :exc:`ModuleNotFoundError` or :exc:`ImportError`
   then head on over to :ref:`installing` section to properly install.
2. Empty Line to increase readability
3. Now we create an instance of :class:`Plugin`, which will let us work with Flow.
4. Empty Line to increase readability
5. Now, in line 5, we use the :func:`Plugin.event` decorator to mark our ``on_query`` coroutine as an event that should be registered.
6. Now in line 6, we define our ``on_query`` event handler, which takes a single argument: ``data`` of the type :class:`~flowpy.query.Query`
7. In line 7, we access the :class:`~flowpy.flow_api.client.FlowLauncherAPI` client, and use its :func:`~flowpy.flow_api.client.FlowLauncherAPI.fuzzy_search` method to tell flow to use fuzzy search to compare the two strings inputted.
   In this case, we are telling Flow to compare whatever the user gave as their query (which we get by the data.:attr:`~flowpy.query.Query.text` attribute), against the string ``Flow``.
8. We are returning a list which we expanded for readability
9. We are putting an :class:`~flowpy.jsonrpc.option.Option` object into the list, but expanding it for readability
10. For the first argument into the :class:`~flowpy.jsonrpc.option.Option` object (which is the title/content of the option), we give a string that's our original text (``Flow``), and after that,the fuzzy search's score. See the :class:`~flowpy.flow_api.fuzzy_search.FuzzySearchResult` class for more information on using the result object.
11. For the second argument into the :class:`~flowpy.jsonrpc.option.Option` object (which is the subtitle of the option), we give a string that tells our user how precise flow thinks it is. See the :class:`~flowpy.flow_api.fuzzy_search.FuzzySearchResult` class for more information on using the result object.
12. For the third argument, we provide title highlight data from the fuzzy search results (this is why we started the option's title/content with our original string). See the `Highlighting section in the FAQ <highlights>` for more information on this.
13. Ending the :class:`~flowpy.jsonrpc.option.Option` object which we expanded for readability
14. Ending the list object that we expanded for readability
15. Empty Line to increase readability
16. Now we call :class:`~flowpy.plugin.Plugin.run` to start the plugin.

Now although we've just made a plugin, we can't use it yet, because it isn't as simple as running the program.
