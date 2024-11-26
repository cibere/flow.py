:orphan:

.. _intro:

Introduction
==============

This is an introduction to the flow.py library, which aims to make it easy for python developers to create advanced plugins for Flow Launcher using it's V2 jsonrpc api.

Prerequisites
---------------

flow.py requires python 3.12 or higher.

.. _installing:

Installing
-----------

To install the stable version, use the following command:

.. note::

    A `Virtual Environment <https://docs.python.org/3/library/venv.html>`__ is recommended to install
    the library.

.. NOTE::
    The ``flow.py`` package on PyPi is NOT the same package

To install flow.py, do the following:

.. code:: sh

    pip install git+https://github.com/cibere/flow.py

Basic Concepts
---------------

Events
~~~~~~

flow.py revolves around a concept called :ref:`events <events>`. An event is something that you listen for, then respond to. For example, when flow starts and runs your plugin, it will send a :ref:`on_initialization <on_initialization>` event that we can listen for.

A quick example code to showcase this:

.. code:: py

    from flowpy import Plugin, Query

    plugin = Plugin()

    @plugin.event
    async def on_initialization():
        # Plugin has started
    
    plugin.run()

Search handlers
~~~~~~~~~~~~~~~

For handling search/query requests with flow.py, you will use :ref:`search handlers <search_handlers>`. See the :ref:`search handlers section <search_handlers>` for an in-depth look at them, but for now, here is a quick version:

You can use the :func:`~flowpy.plugin.Plugin.search` decorator to register a search handler, with an async callback. The callback takes a single argument (:class:`~flowpy.query.Query`), and returns an :class:`~flowpy.jsonrpc.results.Result` object, a list of :class:`~flowpy.jsonrpc.results.Result` objects, or anything that will get casted to a string and converted into an :class:`~flowpy.jsonrpc.results.Result` object.

.. NOTE::
    Unlike :func:`~flowpy.plugin.Plugin.event`, with :func:`~flowpy.plugin.Plugin.search` you must call the decorator, as there are optional arguments that could be passed.

.. code:: py
    
    plugin = Plugin()
    
    @plugin.search()
    async def my_search_handler(query):
        return "Hello!"

Results
~~~~~~~

You can use the :class:`~flowpy.jsonrpc.results.Result` object constructor to pass most options.

.. NOTE::
    For handling what happens when the result gets clicked or customizing the context menu, subclass the object and override the methods. See :class:`~flowpy.jsonrpc.results.Result` for more info.

.. code:: py
    
    plugin = Plugin()
    
    @plugin.search()
    async def my_search_handler(query):
        return Option(
            title=f"Your text: {query.text}",
            sub="boo",
            copy_text=query.text
        )