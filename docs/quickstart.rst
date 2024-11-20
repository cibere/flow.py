:orphan:

.. _quickstart:

Quickstart
============

This page gives a brief introduction to the library. It assumes you have the library installed,
if you don't check the :ref:`installing` portion.

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


There's a lot going on here, so let's walk you through it step by step.

1. The first line just imports the library, if this raises a :exc:`ModuleNotFoundError` or :exc:`ImportError`
   then head on over to :ref:`installing` section to properly install.
2. Next, we create an instance of :class:`Plugin`, which will let us work with Flow.
3. Now we will use the :func:`Plugin.event` decorator to mark our ``on_query`` coroutine as an event that should be registered.

