.. _events:

Event Reference
===========

There are two main ways to register events.

The first way is by using the :func:`~flowpy.plugin.Plugin.event` decorator using your :class:`~flowpy.plugin.Plugin` instance. For example: ::

    @plugin.event
    async def on_initialization():
        print('Ready!')

The second way is by using the :ref:`@subclassed_event <subclassed_event>` decorator inside of a :class:`~flowpy.plugin.Plugin` subclass. For example: ::

    class MyPlugin(Plugin):
        @subclassed_event
        async def on_initialization(self):
            print('Ready!')

.. warning::

    All the events must be a |coroutine_link|_. If they aren't, then you might get unexpected
    errors. In order to turn a function into a coroutine they must be ``async def``
    functions.

API Events
----------
These events are triggered by flow

on_initialization
~~~~~~~~~~~~~~~~~

.. function:: async def on_initialization()

    Called when the plugin gets initialized.

.. _on_query:

on_query
~~~~~~~~

.. function:: async def on_query(data)

    Called when flow says a query request.

    :param data: The query data.
    :type data: :class:`~flowpy.query.Query`
    :rtype: list[:class:`~flowpy.jsonrpc.option.Option`]
    :yields: :class:`~flowpy.jsonrpc.option.Option`

.. _on_context_menu:

on_context_menu
~~~~~~~~~~~~~~~

.. function:: async def on_context_menu(data)

    Called when flow sends a context menu request

    :param data: The context menu data from :attr:`~flowpy.jsonrpc.option.Option.context_data`
    :type data: list[Any]
    :rtype: list[:class:`~flowpy.jsonrpc.option.Option`]
    :yields: :class:`~flowpy.jsonrpc.option.Option`

Error Handling Events
---------------------
These events are triggered by flow.py to handle errors

on_error
~~~~~~~~

.. function:: async def on_error(event, error, *args, **kwargs)

    This is called when an error occurs inside of another event.

    :param event: The name of the event
    :type event: :class:`str`
    :param error: The error that occured
    :type error: :class:`Exception`
    :param *args: The positional arguments that were passed to the event
    :param **kwargs: The keyword arguments that were passed to the event
    :returns: Any valid response object for the given event
    :rtype: :class:`~flowpy.jsonrpc.responses.BaseResponse`

on_action_error
~~~~~~~~~~~~~~~

.. function:: async def on_action_error(action_name, error)

    This is called when an error occurs within an action

    :param action_name: The action's name (see :attr:`~flowpy.jsonrpc.option.Action.name` for more info)
    :type action_name: :class:`str`
    :param error: The error that occured
    :type error: :class:`Exception`
    :returns: The response to be returned to flow. Use :class:`~flowpy.jsonrpc.responses.ExecuteResponse` if the error was successfully handled, use :class:`~flowpy.jsonrpc.responses.ErrorResponse` if the error was not successfully handled.
    :rtype: :class:`~flowpy.jsonrpc.responses.ExecuteResponse` | :class:`~flowpy.jsonrpc.responses.ErrorResponse`