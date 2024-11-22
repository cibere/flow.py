Plugin
===========

.. autoclass:: flowpy.plugin.Plugin
    :members:

.. automethod:: Plugin.event()
    :decorator:

.. automethod:: Plugin.search()
    :decorator:

.. _subclassed_event:

subclassed_event
~~~~~~~~~~~~~~~~

.. function:: @subclassed_event

    A decorator that registers an event to listen for.
    
    All events must be a :ref:`coroutine <coroutine>`.

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

.. _subclassed_search:

subclassed_search
~~~~~~~~~~~~~~~~

.. function:: @subclassed_search

    All search handlers must be a :ref:`coroutine <coroutine>`. See the :ref:`search handler section <search_handlers>` for more information about using search handlers.

    .. NOTE::
        This is to be used inside of a :class:`~flowpy.plugin.Plugin` subclass, use the :func:`~flowpy.plugin.Plugin.search` decorator if it will be used outside of a subclass.

    Parameters
    ----------
    condition: Optional[:ref:`condition <condition_example>`]
        The condition to determine which queries this handler should run on. If given, this should be the only argument given.
    text: Optional[:class:`str`]
        A kwarg to quickly add a :class:`~flowpy.conditions.PlainTextCondition`. If given, this should be the only argument given.
    pattern: Optional[:class:`re.Pattern`]
        A kwarg to quickly add a :class:`~flowpy.conditions.RegexCondition`. If given, this should be the only argument given.

    Example
    ---------

    .. code-block:: python3

        class MyPlugin(Plugin):
            @subclassed_search()
            async def example_search_handler(self, data: Query):
                return "This is a result!"


Classes
~~~~~~~

.. autoclass:: flowpy.settings.Settings
    :members:

.. autoclass:: flowpy.query.Query
    :members: