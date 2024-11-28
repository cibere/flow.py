Whats New
==========

This page keeps a detailed human friendly rendering of what's new and changed in specific versions.

v0.0.5a
-------

New Features
~~~~~~~~~~~~~

- Add :func:`~flogin.plugin.Plugin.register_search_handlers`
- Add the :doc:`whats_new` section in the docs

Bug Fixes
~~~~~~~~~

- Fixed bug with the `create plugin.json <cli-create-plugin-json>`_ CLI command dumping the wrong data.
- Add the missing dependency `click <https://pypi.org/project/click/>`_
- Fix bug where :attr:`~flogin.search_handler.SearchHandler.plugin` is ``None`` when :obj:`~flogin.search_handler.SearchHandler.condition` is ran.