flow.py
========
A wrapper for Flow Lancher's V2 python api using jsonrpc.

.. WARNING::
    This library is still in alpha development, so expect breaking changes

Key Features
-------------

- Modern Pythonic API using ``async`` and ``await``.
- Fully Typed
- Easy to use with an object oriented design

Installing
----------

**Python 3.12 or higher is required**

To install the stable version, use the following command:

.. note::

    A `Virtual Environment <https://docs.python.org/3/library/venv.html>`__ is recommended to install
    the library, especially on Linux where the system Python is externally managed and restricts which
    packages you can install on it.


.. code:: sh

    pip install -U flow.py

To install the development version, do the following:

.. code:: sh

    pip install git+https://github.com/cibere/flow.py

Basic Example
-------------
.. code:: py

    from flowpy import Option, Plugin, Query

    plugin = Plugin()

    @plugin.event
    async def on_query(data: Query):
        yield Option(f"You wrote {data.text}")
    
    plugin.run()

You can find more examples in the examples directory.

Links
------

- `Documentation <https://flowpy.readthedocs.io/en/latest/index.html>`_
- `Flow Launcher's Official Discord Server <https://discord.gg/QDbDfUJaGH>`_

Contributing
============
Contributions are greatly appriciated, I just have a couple of requests:

1. Your code is run through isort and black
2. Your code is properly typed
3. Your code is tested
4. Your code is documented