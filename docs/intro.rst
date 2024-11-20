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

.. code:: sh

    pip install -U flow.py

To install the development version, do the following:

.. code:: sh

    pip install git+https://github.com/cibere/flow.py

Basic Concepts
---------------

Events
~~~~~~

flow.py revolves around a concept called :ref:`events <events>`. An event is something that you listen for, then respond to. For example, when flow sends a query request, you can use the :ref:`on_query <on_query>` event to listen for, and respond to the request.

A quick example code to showcase this:

.. code:: py

    from flowpy import Option, Plugin, Query

    plugin = Plugin()

    @plugin.event
    async def on_query(data: Query):
        return [Option(f"You wrote {data.text}")]
    
    plugin.run()

Options & Actions
~~~~~~~~~~~~~~~~~

When flow sends a query or context menu request, you'll receive them via the :ref:`on_query <on_query>` and :ref:`on_context_menu <on_context_menu>` events. To respond to these requests, you give them a list of :class:`~flowpy.jsonrpc.option.Option` objects, which in the case of a query request, acts as the user's results.

You can use an :class:`~flowpy.jsonrpc.option.Action` to wrap the :ref:`coroutine <coroutine>` that you want to run when a user clicks on the :class:`~flowpy.jsonrpc.option.Option` that the :class:`~flowpy.jsonrpc.option.Action` has been assigned to via the :attr:`~flowpy.jsonrpc.option.Option.action` parameter/attribute.