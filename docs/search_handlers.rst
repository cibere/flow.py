.. _search_handlers:

Search Handlers
===============
The easy and intuative way of handling query/search requests.

Search Handler Callback
------------------------

.. function:: async def search_handler_callback(query)

    This is an scheme of a basic search handler callback that returns items.

    See the :ref:`registering search handlers section <register_search_handler>` for information on how to register your search handler.

    Flow.py will attemp to convert whatever the callback returns into a list of options. If a dictionary is given, flow.py will try and convert it into an :class:`~flowpy.jsonrpc.option.Option` via :func:`~flowpy.jsonrpc.option.Option.from_dict`
    
    The callback can also be an async iterator, and yield the results.

    :param query: The query data
    :type query: :class:`~flowpy.query.Query`
    :rtype: :class:`~flowpy.jsonrpc.option.Option` | list[:class:`~flowpy.jsonrpc.option.Option`] | dict | str | int | Any
    :yields: :class:`~flowpy.jsonrpc.option.Option` | dict | str | int | Any
    :returns: Flow.py will take the output in whatever form it is in, and try its best to convert it into a list of options. Worst case, it casts the item to a string and handles it accordingly.

.. code:: py

    # Return a string, which gets turned into a option
    async def search_handler_callback_example(query):
        return "This is a string"
    # Flow.py will return a single option to flow launcher, which will look something like this:
    # Option("This is a string")

.. code:: py

    # Return a list of strings, which gets turned into a list of strings
    async def search_handler_callback_example(query):
        return ["Foo", "Bar", "Apple", "Pear"]
    # Flow.py will return a list of options to flow launcher, which will look something like this:
    # [
    #   Option("Foo"),
    #   Option("Bar"),
    #   Option("Apple"),
    #   Option("Pear"),
    # ]

.. code:: py

    # Return an int, which gets casted to a string and turned into an option.
    async def search_handler_callback_example(query):
        return 25
    # Flow.py will return a single option to flow launcher, which will look something like this:
    # Option(str(25))

.. code:: py

    # yield a couple of numbers
    async def search_handler_callback_example(query):
        yield 2
        yield 3
        yield 25
        yield 30
    # Flow.py will return a list of options to flow launcher, which will look something like this:
    # [
    #   Option(str(2)),
    #   Option(str(3)),
    #   Option(str(25)),
    #   Option(str(30)),
    # ]

Conditions
-----------

Flow.py uses condition functions to determine which handler should be used on a certain query. A condition function should take a single parameter (:class:`~flowpy.query.Query`), and return a bool. ``True`` means the search handler that this condition is associated with should be used on this query, and ``False`` means that the search handler shouldn't be used on this query. See the :ref:`builtin conditions section <builtin_search_conditions>` of this page's api reference for a list of builtin conditions.

.. _condition_example:

Condition Example
~~~~~~~~~~~~~~~~~

.. function:: def condition(query)

    This is called when flow.py is determining if a certain query handler should be used for a certain query or not.

    :param query: The query that will be give to the search handler
    :type query: :class:`~flowpy.query.Query`
    :rtype: :class:`bool`
    :returns: A bool. ``True`` means the search handler that this condition is associated with should be used on this query, and ``False`` means that the search handler shouldn't be used on this query.

.. _register_search_handler:

Registering Handlers
--------------------

There are 3 main ways to register handlers:

1. :ref:`Using the plugin.search decorator <register_search_handler_by_plugin.search_deco>`

2. :ref:`Using the subclassed_search decorator <register_search_handler_by_subclassed_search_deco>`

3. :ref:`Manually create and register the handler <manaully_register_search_handler>`

.. _register_search_handler_by_plugin.search_deco:

Plugin.search decorator
~~~~~~~~~~~~~~~~~~~~~~~
If you want to create a handler outside of your :class:`~flowpy.plugin.Plugin` class using a decorator, you can use the :func:`~flowpy.plugin.Plugin.search` decorator. ::

    @plugin.search()
    async def my_handler(query: Query):
        return f"Your query was: {query.text}"

.. _register_search_handler_by_subclassed_search_deco:

subclassed_search decorator
~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you want to create a handler inside of your :class:`~flowpy.plugin.Plugin` class using a decorator, you can use the :ref:`subclassed_search <subclassed_search>` decorator. ::

    class MyPlugin(Plugin):
        @subclassed_search()
        async def my_handler(self, query: Query):
            return f"Your query was: {query.text}"

.. _manaully_register_search_handler:

Manually Create Class
~~~~~~~~~~~~~~~~~~~~~
If you manually created a :class:`~flowpy.search_handler.SearchHandler` instance and you want to register it, you can use the :func:`~flowpy.plugin.Plugin.register_search_handler` function. ::

    handler = SearchHandler(callback, condition)
    plugin.register_search_handler(handler)

API Reference
-------------

Search Handlers
~~~~~~~~~~~~~~~~

.. autoclass:: flowpy.search_handler.SearchHandler
    :members:

.. _builtin_search_conditions:

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