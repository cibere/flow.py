Whats New
==========

This page keeps a detailed human friendly rendering of what's new and changed in specific versions.

v0.1.0
------

Breaking Changes
~~~~~~~~~~~~~~~~

- Move :class:`flogin.jsonrpc.results.Glyph` support from :attr:`flogin.jsonrpc.results.Result.icon` to :class:`flogin.jsonrpc.results.Result.gylph`
- The :class:`flogin.conditions.MultiCondition` constructor has gone from taking a list of conditions to being a varargs argument.
- Return ``None`` if a setting is not found in :class:`flogin.settings.Setting`
    - Remove ``flogin.errors.SettingNotFound``
- Rewrite the CLI commands

New Features
~~~~~~~~~~~~

- Add ``Query.__repr__``
- Let :func:`flogin.search_handler.SearchHandler.callback` and :func:`flogin.jsonrpc.results.Result.context_menu` return ``None``
- Add ``Generic`` to :class:`flogin.search_handler.SearchHandler` for :attr:`flogin.search_handler.SearchHandler.plugin`
- Add ``Generic`` to :class:`flogin.jsonrpc.results.Result` for :attr:`flogin.jsonrpc.results.Result.plugin`
- Update ``Query.__init__`` to allow for an easier time manually creating query objects.
- Add the ability to supply a default into ``flogin.errors.SettingNotFound.__getitem__``
- Add a generic to :class:`flogin.plugin.Plugin` for a custom :class:`flogin.settings.Settings` class.
- Document the generic in :class:`flogin.jsonrpc.results.Result` for a custom plugin class.
- Document the generic in :class:`flogin.search_handler.SearchHandler.plugin` for a custom plugin class.
- Document the generic in :class:`flogin.query.Query` for :attr:`flogin.query.Query.condition_data`

Bug Fixes
~~~~~~~~~

- Fix bug where :func:`FlowLauncherAPI.update_results` does not register the results, so callbacks do not get triggered.
- Fix typing bug with :func:`flogin.plugin.Plugin.register_search_handlers` and :func:`flogin.plugin.Plugin.register_search_handler` due to :class:`flogin.search_handler.SearchHandler` being a generic.
- Fix bug where ``Glyph`` was not included in ``ResultConstructorArgs``
- Fix bug with the ``PluginT`` TypeVar not being marked as covariant

Removals
~~~~~~~~~
- Remove the ``CLI`` docs section
- Remove `click <https://pypi.org/project/click>`_ as a dependency.

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