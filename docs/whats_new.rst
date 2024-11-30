Whats New
==========

This page keeps a detailed human friendly rendering of what's new and changed in specific versions.

v0.0.5a
-------

New Features
~~~~~~~~~~~~~

- Add :func:`~flogin.plugin.Plugin.register_search_handlers`
- Add the :doc:`whats_new` section in the docs
- Add :func:`~flogin.plugin.Plugin.register_event`
- Add :ref:`flogin gh gitignore <create_gitignore_cli>` CLI command
- Add :class:`~flogin.jsonrpc.glyph.Glyph`
    - Allow :class:`~flogin.jsonrpc.glyph.Glyph` objects in :attr:`~flogin.jsonrpc.results.Result.icon`
- Add :attr:`~flogin.jsonrpc.results.Result.rounded_icon`
- Add :class:`flogin.jsonrpc.results.ResultPreview`
    - Add :attr:`~flogin.jsonrpc.results.Result.preview`
- Add :class:`flogin.jsonrpc.results.ProgressBar`
    - Add :attr:`flogin.jsonrpc.results.Result.progress_bar`
- Add :attr:`flogin.jsonrpc.results.Result.auto_complete_text`
- Add :ref:`flogin create settings <cli-create-settings-template>` CLI command

Bug Fixes
~~~~~~~~~

- Fixed bug with the `create plugin.json <cli-create-plugin-json>`_ CLI command dumping the wrong data.
- Add the missing dependency `click <https://pypi.org/project/click/>`_
- Fix bug where :attr:`~flogin.search_handler.SearchHandler.plugin` is ``None`` when :obj:`~flogin.search_handler.SearchHandler.condition` is ran.
- Fix an ``AttributeError`` that gets raised in a couple of :class:`~flogin.flow_api.client.FlowLauncherAPI` methods
- Log fatal errors that cause startup crashes to prevent them from being hidden.
- Fix bug where ``rounded_icon`` was not present in ``ResultConstructorArgs``
- Fix a ``NameError`` that gets raised in the default :func:`flogin.jsonrpc.results.Result.callback`