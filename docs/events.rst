.. _events:

Event Reference
================

You can register an event using the :func:`~flowpy.plugin.Plugin.event` decorator using your :class:`~flowpy.plugin.Plugin` instance. For example: ::

    @plugin.event
    async def on_initialization():
        print('Ready!')

.. warning::

    All the events must be a |coroutine_link|_. If they aren't, then you might get unexpected
    errors. In order to turn a function into a coroutine they must be ``async def``
    functions.

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
    :param args: The positional arguments that were passed to the event
    :param kwargs: The keyword arguments that were passed to the event
    :returns: Any valid response object for the given event
    :rtype: :class:`~flowpy.jsonrpc.responses.BaseResponse`