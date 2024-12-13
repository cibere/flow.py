.. module:: flogin

API Reference
=============

Plugin
------

.. autoclass:: flogin.plugin.Plugin
    :members:

.. autodecorator:: Plugin.event()

.. autodecorator:: Plugin.search()

Classes
~~~~~~~

.. autoclass:: flogin.settings.Settings
    :members:

.. autoclass:: flogin.query.Query
    :members:

JSON RPC
--------

Results
~~~~~~~

.. autoclass:: flogin.jsonrpc.results.Result
    :members:
    
.. autoclass:: flogin.jsonrpc.results.ResultPreview
    :members:

.. autoclass:: flogin.jsonrpc.results.ProgressBar
    :members:
    
.. autoclass:: flogin.jsonrpc.results.Glyph
    :members:

Responses
~~~~~~~~~

.. autoclass:: flogin.jsonrpc.responses.BaseResponse
    :members:

.. autoclass:: flogin.jsonrpc.responses.ErrorResponse
    :members:

.. autoclass:: flogin.jsonrpc.responses.QueryResponse
    :members:

.. autoclass:: flogin.jsonrpc.responses.ExecuteResponse
    :members:

.. _search_handlers_api_reference:

Search Handlers
---------------

.. autoclass:: flogin.search_handler.SearchHandler
    :members:

.. _builtin_search_conditions:

Builtin Search Conditions
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: flogin.conditions.PlainTextCondition
    :members:

.. autoclass:: flogin.conditions.RegexCondition
    :members:

.. autoclass:: flogin.conditions.KeywordCondition
    :members:

.. autoclass:: flogin.conditions.MultiCondition
    :members:


Flow API
----------

Client
~~~~~~~~

.. autoclass:: flogin.flow_api.client.FlowLauncherAPI
    :members:

Classes
~~~~~~~~

.. autoclass:: flogin.flow_api.fuzzy_search.FuzzySearchResult
    :members:

.. autoclass:: flogin.flow_api.plugin_metadata.PluginMetadata
    :members:

Errors
-----------

Plugin Errors
~~~~~~~~~~~~~

.. autoclass:: flogin.errors.PluginException
    :members:

.. autoclass:: flogin.errors.SettingNotFound
    :members:

.. autoclass:: flogin.errors.PluginNotInitialized
    :members:

JSON-RPC Errors
~~~~~~~~~~~~~~~

.. autoclass:: flogin.jsonrpc.errors.JsonRPCException
    :members:

.. autoclass:: flogin.jsonrpc.errors.JsonRPCVersionMismatch
    :members:

Testing
-------

.. autoclass:: flogin.testing.plugin_tester.PluginTester
    :members:

Utils
-----

.. autofunction:: flogin.utils.setup_logging

.. autofunction:: flogin.utils.coro_or_gen

.. attribute:: flogin.utils.MISSING

    A type safe sentinel used in the library to represent something as missing. Used to distinguish from ``None`` values.

.. decorator:: flogin.utils.cached_property()

    A version of :func:`functools.cached_property` that is safe for async programs.

    Example
    --------
    .. code-block:: python3

        class Foo:
            @utils.cached_property
            def bar(self):
                ...

.. autodecorator:: flogin.utils.cached_coro()

.. autodecorator:: flogin.utils.cached_gen()