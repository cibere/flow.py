flogin
=======
A wrapper for Flow Lancher's V2 jsonrpc api using python, to easily and quickly make **Flo**\ w launcher plu\ **gin**\ s.

Flogin's `documentation can be viewed online <https://flogin.readthedocs.io/en/latest/>`_

.. WARNING::
    This library is still in alpha development, so expect breaking changes

Key Features
-------------

- Modern Pythonic API using ``async`` and ``await``.
- Fully Typed
- Easy to use with an object oriented design

Installing
----------

**Python 3.11 or higher is required**

To install flogin, do the following:

.. code:: sh

    pip install flogin

To install the development version, ensure `git <https://git-scm.com/>`_ is installed, then do the following:

.. code:: sh

    pip install git+https://github.com/cibere/flogin

Basic Example
-------------
.. code:: py

    from flogin import Plugin, Query

    plugin = Plugin()

    @plugin.event
    async def on_query(data: Query):
        return f"You wrote {data.text}"
    
    plugin.run()

You can find more examples in the examples directory.

Links
------

- `Documentation <https://flogin.readthedocs.io/en/latest/index.html>`_
- `Flow Launcher's Official Discord Server <https://discord.gg/QDbDfUJaGH>`_

Contributing
============
Contributions are greatly appriciated, I just have a couple of requests:

1. Your code is run through isort and black
2. Your code is properly typed
3. Your code is tested
4. Your code is documented