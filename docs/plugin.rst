Plugin
===========

.. autoclass:: flowpy.plugin.Plugin
    :members:

.. automethod:: Plugin.event()
    :decorator:

.. _subclassed_event:

subclassed_event
~~~~~~~~~~~~~~~~

.. function:: @subclassed_event

    A decorator that registers an event to listen for.
    
    Aside from the `query` and `context_menu` events, all events must be a :ref:`coroutine <coroutine>`.

    .. NOTE::
        See the :ref:`event reference <events>` to see what valid events there are.
    
    .. NOTE::
        This is to be used within a :class:`~flowpy.plugin.Plugin` subclass, use :func:`~flowpy.plugin.Plugin.event` if it will be used outside of a subclass.
    
    Example
    ---------

    .. code-block:: python3

        class MyPlugin(Plugin):
            @subclassed_event
            async def on_initialization(self):
                print('Ready!')

Classes
~~~~~~~

.. autoclass:: flowpy.settings.Settings
    :members:

.. autoclass:: flowpy.query.Query
    :members: