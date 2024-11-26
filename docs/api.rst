API Reference
=============

Plugin
------

.. autoclass:: flowpy.plugin.Plugin
    :members:

.. autodecorator:: Plugin.event()

.. autodecorator:: Plugin.search()

Classes
~~~~~~~

.. autoclass:: flowpy.settings.Settings
    :members:

.. autoclass:: flowpy.query.Query
    :members:

JSON RPC
--------

Result
~~~~~~

.. autoclass:: flowpy.jsonrpc.results.Result
    :members:

Responses
~~~~~~~~~

.. autoclass:: flowpy.jsonrpc.responses.BaseResponse
    :members:

.. autoclass:: flowpy.jsonrpc.responses.ErrorResponse
    :members:

.. autoclass:: flowpy.jsonrpc.responses.QueryResponse
    :members:

.. autoclass:: flowpy.jsonrpc.responses.ExecuteResponse
    :members:

Flow API
----------

Client
~~~~~~~~

.. autoclass:: flowpy.flow_api.client.FlowLauncherAPI
    :members:

Classes
~~~~~~~~

.. autoclass:: flowpy.flow_api.fuzzy_search.FuzzySearchResult
    :members:

.. autoclass:: flowpy.flow_api.plugin_metadata.PluginMetadata
    :members:

Search Handlers
---------------

.. autoclass:: flowpy.search_handler.SearchHandler
    :members:

.. _builtin_search_conditions:

Builtin Search Conditions
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: flowpy.conditions.PlainTextCondition
    :members:

.. autoclass:: flowpy.conditions.RegexCondition
    :members:

.. autoclass:: flowpy.conditions.KeywordCondition
    :members:

.. autoclass:: flowpy.conditions.MultiCondition
    :members:

Errors
-----------

Plugin Errors
~~~~~~~~~~~~~

.. autoclass:: flowpy.errors.PluginException
    :members:

.. autoclass:: flowpy.errors.SettingNotFound
    :members:

.. autoclass:: flowpy.errors.PluginNotInitialized
    :members:

JSON-RPC Errors
~~~~~~~~~~~~~~~

.. autoclass:: flowpy.jsonrpc.errors.JsonRPCException
    :members:

.. autoclass:: flowpy.jsonrpc.errors.JsonRPCVersionMismatch
    :members:

Utils
-----

.. autofunction:: flowpy.utils.setup_logging

.. autofunction:: flowpy.utils.coro_or_gen

.. attribute:: flowpy.utils.MISSING

    A type safe sentinel used in the library to represent something as missing. Used to distinguish from ``None`` values.

.. decorator:: flowpy.utils.cached_property()

    A version of :func:`functools.cached_property` that is safe for async programs.

    Example
    --------
    .. code-block:: python3

        class Foo:
            @utils.cached_property
            def bar(self):
                ...

.. autodecorator:: flowpy.utils.cached_coro()