Whats New
==========

This page keeps a detailed human friendly rendering of what's new and changed in specific versions.

v0.1.0
------

Breaking Changes
~~~~~~~~~~~~~~~~

- Move :class:`flogin.jsonrpc.results.Glyph` support from :attr:`flogin.jsonrpc.results.Result.icon` to :class:`flogin.jsonrpc.results.Result.gylph`

New Features
~~~~~~~~~~~~

- Add ``Query.__repr__``
- Let :func:`flogin.search_handler.SearchHandler.callback` and :func:`flogin.jsonrpc.results.Result.context_menu` return ``None``
- Add ``Generic`` to :class:`flogin.search_handler.SearchHandler` for :attr:`flogin.search_handler.SearchHandler.plugin`
- Add ``Generic`` to :class:`flogin.jsonrpc.results.Result` for :attr:`flogin.jsonrpc.results.Result.plugin`
- Update ``Query.__init__`` to allow for an easier time manually creating query objects.

Bug Fixes
~~~~~~~~~

- Fix bug where :func:`FlowLauncherAPI.update_results` does not register the results, so callbacks do not get triggered.

v0.0.5
-------

New Features
~~~~~~~~~~~~~

- Add :func:`flogin.plugin.Plugin.register_search_handlers`
- Add the :doc:`whats_new` section in the docs
- Add :func:`flogin.plugin.Plugin.register_event`
- Add :ref:`flogin gh gitignore <create_gitignore_cli>` CLI command
- Add :class:`flogin.jsonrpc.results.ResultPreview`
    - Add :attr:`~flogin.jsonrpc.results.Result.preview`
- Add :class:`flogin.jsonrpc.results.ProgressBar`
    - Add :attr:`flogin.jsonrpc.results.Result.progress_bar`
- Add :attr:`flogin.jsonrpc.results.Result.auto_complete_text`
- Add :class:`flogin.jsonrpc.results.Glyph`
    - Allow :class:`~flogin.jsonrpc.results.Glyph` objects in :attr:`flogin.jsonrpc.results.Result.icon`
- Add :attr:`flogin.jsonrpc.results.Result.rounded_icon`
- Add :ref:`flogin create settings <cli-create-settings-template>` CLI command
- Add :func:`flogin.utils.cached_gen`

Bug Fixes
~~~~~~~~~

- Fixed bug with the `create plugin.json <cli-create-plugin-json>`_ CLI command dumping the wrong data.
- Add the missing dependency `click <https://pypi.org/project/click/>`_
- Fix bug where :attr:`flogin.search_handler.SearchHandler.plugin` is ``None`` when :obj:`flogin.search_handler.SearchHandler.condition` is ran.
- Fix an ``AttributeError`` that gets raised in a couple of :class:`~flogin.flow_api.client.FlowLauncherAPI` methods
- Log fatal errors that cause startup crashes to prevent them from being hidden.
- Fix bug where ``rounded_icon`` was not present in ``ResultConstructorArgs``
- Fix a ``NameError`` that gets raised in the default :func:`flogin.jsonrpc.results.Result.callback`
- Fix bug where :attr:`flogin.plugin.Plugin.settings` will be replaced with a new :class:`~flogin.settings.Settings` instance every time a new query request is received, preventing making setting changes.