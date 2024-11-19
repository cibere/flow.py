Event Reference
===========

.. warning::

    All the events must be a |coroutine_link|_. If they aren't, then you might get unexpected
    errors. In order to turn a function into a coroutine they must be ``async def``
    functions.

API Events
----------
These events are triggered by flow

.. function:: async def on_query(data)

    Called when flow says a query request.

    :param data: The query data.
    :type data: :class:`~flowpy.query.Query`
    :rtype: list[:class:`~flowpy.jsonrpc.option.Option`]
    :yields: :class:`~flowpy.jsonrpc.option.Option`
    
.. function:: async def on_context_menu(data)

    Called when flow sends a context menu request

    :param data: The context menu data from :attr:`~flowpy.jsonrpc.option.Option.context_data`
    :type data: list[:class:`Any`]
    :rtype: list[:class:`~flowpy.jsonrpc.option.Option`]
    :yields: :class:`~flowpy.jsonrpc.option.Option`
