Flow API
===========

Event Reference
---------------

.. warning::

    All the events must be a |coroutine_link|_. If they aren't, then you might get unexpected
    errors. In order to turn a function into a coroutine they must be ``async def``
    functions.

API Events
~~~~~~~~~~
These events are triggered by flow

.. function:: on_query(data)

    Called when flow says a query request.

    :param data: The query data.
    :type data: :class:`Query`
    :returns: list[:class:`Option`]
    :yields: :class:`Option`

.. function:: on_context_menu(data)

    Called when flow sends a context menu request

    :param data: The context menu data from :attr:`Option.context_data`
    :type data: list[:class:`Any`]
    :returns: list[:class:`Option`]
    :yields: :class:`Option`