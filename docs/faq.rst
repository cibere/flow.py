.. _faq:

Frequently Asked Questions
===========================

This is a list of Frequently Asked Questions regarding using ``flow.py`` and its extension modules. Feel free to suggest a
new question or submit one via pull requests.

Coroutines
------------

Questions regarding coroutines and asyncio belong here.

.. NOTE::
    Credits for the ``Coroutines`` section goes to `discord.py <https://discordpy.readthedocs.io/en/latest/faq.html?highlight=on_error#coroutines>`_

What is a coroutine?
~~~~~~~~~~~~~~~~~~~~~~

A |coroutine_link|_ is a function that must be invoked with ``await`` or ``yield from``. When Python encounters an ``await`` it stops
the function's execution at that point and works on other things until it comes back to that point and finishes off its work.
This allows for your program to be doing multiple things at the same time without using threads or complicated
multiprocessing.

**If you forget to await a coroutine then the coroutine will not run. Never forget to await a coroutine.**

Where can I use ``await``\?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can only use ``await`` inside ``async def`` functions and nowhere else.

What does "blocking" mean?
~~~~~~~~~~~~~~~~~~~~~~~~~~~

In asynchronous programming a blocking call is essentially all the parts of the function that are not ``await``. Do not
despair however, because not all forms of blocking are bad! Using blocking calls is inevitable, but you must work to make
sure that you don't excessively block functions. Remember, if you block for too long then your bot will freeze since it has
not stopped the function's execution at that point to do other things.

A common source of blocking for too long is something like :func:`time.sleep`. Don't do that. Use :func:`asyncio.sleep`
instead. Similar to this example: ::

    # bad
    time.sleep(10)

    # good
    await asyncio.sleep(10)

Another common source of blocking for too long is using HTTP requests with the famous module :doc:`req:index`.
While :doc:`req:index` is an amazing module for non-asynchronous programming, it is not a good choice for
:mod:`asyncio` because certain requests can block the event loop too long. Instead, use the :doc:`aiohttp <aio:index>` library which
is installed on the side with this library.

Consider the following example: ::

    # bad
    r = requests.get('https://httpbin.org/get')
    if r.status_code == 200:
        js = r.json()
        yield Option(f"User Agent: {js['headers']['User-Agent']}")

    # good
    async with aiohttp.ClientSession() as session:
        async with session.get('https://httpbin.org/get') as r:
            if r.status == 200:
                js = await r.json()
                yield Option(f"User Agent: {js['headers']['User-Agent']}")

General
---------

General questions regarding library usage belong here.

Where can I find usage examples?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Example code can be found in the `examples folder <https://github.com/cibere/flow.py/tree/master/examples>`_
in the repository.

Where can I get help with using the library?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can ask questions in `flow's official discord server <https://discord.gg/QDbDfUJaGH>`_