.. _ctx_menu_handlers:

Context Menu Handlers
=====================
A simple and easy way of handling context menu requests.

Context Menu Handler Callback
------------------------

.. function:: async def context_menu_callback(*args, **kwargs)

    This is an scheme of a basic context menu handler callback that returns items.

    See the :ref:`registering context menu handlers section <register_context_menu>` for information on how to register your context menu handler.

    Flow.py will attemp to convert whatever the callback returns into a list of options. If a dictionary is given, flow.py will try and convert it into an :class:`~flowpy.jsonrpc.option.Option` via :func:`~flowpy.jsonrpc.option.Option.from_dict`
    
    The callback can also be an async iterator, and yield the results.

    .. NOTE::
        Besides the parameters, the context menu callback is the exact same as a search callback. See the :ref:`Search Handlers Section <search_handlers>` for more information about these callbacks, including examples.

    :param args: Any positional arguments to be passed
    :param kwargs: Any keyword arguments to be passed.
    :rtype: :class:`~flowpy.jsonrpc.option.Option` | list[:class:`~flowpy.jsonrpc.option.Option`] | dict | str | int | Any
    :yields: :class:`~flowpy.jsonrpc.option.Option` | dict | str | int | Any
    :returns: Flow.py will take the output in whatever form it is in, and try its best to convert it into a list of options. Worst case, it casts the item to a string and handles it accordingly.


.. _register_context_menu:

Registering Handlers
--------------------

There are 2 main ways to register handlers:

1. :ref:`Using the plugin.context_menu decorator <register_ctx_menu_handler_by_plugin.ctx_menu_deco>`

2. :ref:`Manually create and register the handler <manaully_register_ctx_menu_handler>`

.. _register_ctx_menu_handler_by_plugin.ctx_menu_deco:

Plugin.search decorator
~~~~~~~~~~~~~~~~~~~~~~~
If you want to create a handler outside of your :class:`~flowpy.plugin.Plugin` class using a decorator, you can use the :func:`~flowpy.plugin.Plugin.context_menu` decorator. ::

    @plugin.context_menu
    async def my_handler(arg: str):
        return f"Hi: {arg}"
    
    # Later on
    Option(..., context_menu_handler=my_handler("some arg"))

.. _manaully_register_ctx_menu_handler:

Manually Create Class
~~~~~~~~~~~~~~~~~~~~~
If you manually created a :class:`~flowpy.context_menu_handler.ContextMenuHandler` instance and you want to register it, you can use the :func:`~flowpy.plugin.Plugin.register_context_menu_handler` function. ::

    async def my_handler(arg: str):
        return f"Hi: {arg}"

    handler = ContextMenuHandler(my_handler, "my_arg")
    plugin.register_context_menu_handler(handler)
    return Option(..., context_menu_handler=handler)

API Reference
-------------

Search Handlers
~~~~~~~~~~~~~~~~

.. autoclass:: flowpy.context_menu_handler.ContextMenuHandler
    :members: