.. _search_handlers:

Search Handlers
===============
The easy and intuative way of handling query/search requests.

Registering Handlers
--------------------

Plugin.search decorator
~~~~~~~~~~~~~~~~~~~~~~~
If you want to create a handler outside of your :class:`~flowpy.plugin.Plugin` class using a decorator, you can use the :func:`~flowpy.plugin.Plugin.search` decorator.
.. code:: py

    @plugin.search()
    async def my_handler(query: Query):
        return f"Your query was: {query.text}"

subclassed_search decorator
~~~~~~~~~~~~~~~~~~~~~~~
If you want to create a handler inside of your :class:`~flowpy.plugin.Plugin` class using a decorator, you can use the `subclassed_search <subclassed_search>` decorator.
.. code:: py

    class MyPlugin(Plugin):
        @subclassed_search()
        async def my_handler(self, query: Query):
            return f"Your query was: {query.text}"

Manually Create Class
~~~~~~~~~~~~~~~~~~~~~
If you manually created a :class:`~flowpy.search_handler.SearchHandler` instance and you want to register it, you can use the :func:`~flowpy.plugin.Plugin.register_search_handler` function.
.. code:: py

    handler = SearchHandler(callback, condition)
    plugin.register_search_handler(handler)

API Reference
-------------

Search Handlers
~~~~~~~~~~~~~~~~

.. autoclass:: flowpy.search_handler.SearchHandler
    :members:

Builtin conditions
~~~~~~~~~~~~~~~~~~

.. autoclass:: flowpy.conditions.PlainTextCondition
    :members:

.. autoclass:: flowpy.conditions.RegexCondition
    :members:

.. autoclass:: flowpy.conditions.KeywordCondition
    :members:

.. autoclass:: flowpy.conditions.MultiCondition
    :members: