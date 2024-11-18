from __future__ import annotations

from typing import TYPE_CHECKING, Any, ParamSpec

from .fuzzy_search import FuzzySearchResult
from .plugin_metadata import PluginMetadata

ATS = ParamSpec("ATS")

if TYPE_CHECKING:
    from ..jsonrpc import ExecuteResponse, JsonRPCClient, Result

__all__ = ("FlowLauncherAPI",)


class FlowLauncherAPI:
    r"""This class is a wrapper around Flow's API to make it easy to make requests and receive results.
    
    .. NOTE:: 
        Do not initialize this class yourself, use :obj:`Plugin.api` to get an instance instead.
    """

    def __init__(self, jsonrpc: JsonRPCClient):
        self.jsonrpc = jsonrpc

    async def __call__(self, method: str, *args: Any, **kwargs: Any) -> ExecuteResponse:
        from ..jsonrpc import ExecuteResponse

        await getattr(self, method)(*args, **kwargs)
        return ExecuteResponse()

    async def fuzzy_search(
        self, text: str, text_to_compare_it_to: str
    ) -> FuzzySearchResult:
        """
        Asks flow how similiar two strings
        """

        from ..jsonrpc import Result  # circular import

        res = await self.jsonrpc.request("FuzzySearch", [text, text_to_compare_it_to])
        assert isinstance(res, Result)
        return FuzzySearchResult(res.data)

    async def change_query(self, new_query: str, requery: bool = False) -> None:
        """
        Change the query in flow launcher's menu
        """

        from ..jsonrpc import Result  # circular import

        res = await self.jsonrpc.request("ChangeQuery", [new_query, requery])
        assert isinstance(res, Result)

    async def show_error_message(self, title: str, text: str) -> None:
        """
        Triggers an error message in a windows notification
        """

        from ..jsonrpc import Result  # circular import

        res = await self.jsonrpc.request("ShowMsgError", [title, text])
        assert isinstance(res, Result)

    async def show_message(
        self,
        title: str,
        text: str,
        icon: str = "",
        use_main_window_as_owner: bool = True,
    ) -> Result:
        """
        Triggers a message via a window's notification
        """

        from ..jsonrpc import Result  # circular import

        res = await self.jsonrpc.request(
            "ShowMsg", [title, text, icon, use_main_window_as_owner]
        )
        assert isinstance(res, Result)
        return res

    async def open_settings_menu(self) -> None:
        """
        This method tells flow to open up the settings menu
        """

        from ..jsonrpc import Result  # circular import

        res = await self.jsonrpc.request("OpenSettingDialog")
        assert isinstance(res, Result)

    async def open_url(self, url: str, in_private: bool = False) -> None:
        """
        Open up a url in the user's preferred browser
        """

        from ..jsonrpc import Result  # circular import

        res = await self.jsonrpc.request("OpenUrl", [url, in_private])
        assert isinstance(res, Result)

    async def run_shell_cmd(self, cmd: str, filename: str = "cmd.exe") -> None:
        """
        Tell flow to run a shell command
        """

        from ..jsonrpc import Result  # circular import

        res = await self.jsonrpc.request("ShellRun", [cmd, filename])
        assert isinstance(res, Result)

    async def restart_flow_launcher(self) -> None:
        """
        This method tells flow launcher to initiate a restart, expect this coro to never finish.
        """

        from ..jsonrpc import Result  # circular import

        res = self.jsonrpc.request("RestartApp")
        assert isinstance(res, Result)

    async def save_all_app_settings(self) -> None:
        """
        This method tells flow to save all app settings.
        """

        from ..jsonrpc import Result  # circular import

        res = await self.jsonrpc.request("SaveAppAllSettings")
        assert isinstance(res, Result)

    async def save_plugin_settings(self) -> Any:
        """
        This method tells flow to save plugin settings
        """

        from ..jsonrpc import Result  # circular import

        res = await self.jsonrpc.request("SavePluginSettings")
        assert isinstance(res, Result)
        return res.data

    async def reload_all_plugin_data(self) -> None:
        """
        This method tells flow to trigger a reload of all plugins.
        """

        from ..jsonrpc import Result  # circular import

        res = await self.jsonrpc.request("ReloadAllPluginDataAsync")
        assert isinstance(res, Result)

    async def show_main_window(self) -> None:
        """
        This method tells flow to show the main window
        """

        from ..jsonrpc import Result  # circular import

        res = await self.jsonrpc.request("ShowMainWindow")
        assert isinstance(res, Result)

    async def hide_main_window(self) -> Any:
        """
        This method tells flow to hide the main window
        """

        from ..jsonrpc import Result  # circular import

        res = await self.jsonrpc.request("HideMainWindow")
        assert isinstance(res, Result)

    async def is_main_window_visible(self) -> bool:
        """
        This method asks flow if the main window is visible

        Returns: bool
        """

        from ..jsonrpc import Result  # circular import

        res = await self.jsonrpc.request("IsMainWindowVisible")
        assert isinstance(res, Result)
        return res.data

    async def check_for_updates(self) -> None:
        """
        This tells flow launcher to check for updates to flow launcher (not your plugin)
        """

        from ..jsonrpc import Result  # circular import

        res = await self.jsonrpc.request("CheckForNewUpdate")
        assert isinstance(res, Result)

    async def get_all_plugins(self) -> list[PluginMetadata]:
        """
        Get the metadata of all plugins that the user has
        """

        from ..jsonrpc import Result  # circular import

        res = await self.jsonrpc.request("GetAllPlugins")
        assert isinstance(res, Result)
        return [PluginMetadata(plugin["metadata"], self) for plugin in res.data]

    async def add_keyword(self, plugin_id: str, keyword: str) -> None:
        """
        Registers a new keyword for a plugin with flow launcher.
        """

        from ..jsonrpc import Result  # circular import

        res = await self.jsonrpc.request("AddActionKeyword", [plugin_id, keyword])
        assert isinstance(res, Result)

    async def remove_keyword(self, plugin_id: str, keyword: str) -> None:
        """
        Registers a new keyword for a plugin with flow launcher.
        """

        from ..jsonrpc import Result  # circular import

        res = await self.jsonrpc.request("RemoveActionKeyword", [plugin_id, keyword])
        assert isinstance(res, Result)

    async def open_directory(self, directory: str, file: str | None = None) -> None:
        """
        Opens up a folder in file explorer. IF a file is provided, the file will be pre-selected.
        """

        from ..jsonrpc import Result  # circular import

        res = await self.jsonrpc.request("OpenDirectory", [directory, file])
        assert isinstance(res, Result)
