from ..jsonrpc import JsonRPCClient, Result
from .fuzzy_search import FuzzySearchResult

__all__ = ("FlowLauncherAPI",)


class FlowLauncherAPI:
    def __init__(self, jsonrpc: JsonRPCClient):
        self.jsonrpc = jsonrpc

    async def fuzzy_search(
        self, text: str, text_to_compare_it_to: str
    ) -> FuzzySearchResult:
        res = await self.jsonrpc.request("FuzzySearch", [text, text_to_compare_it_to])
        assert isinstance(res, Result)
        return FuzzySearchResult(res.data)

    async def change_query(self, new_query: str, requery: bool = False) -> None:
        res = await self.jsonrpc.request("ChangeQuery", [new_query, requery])
        assert isinstance(res, Result)

    async def copy_to_clipboard(
        self, text: str, direct_copy: bool = False, show_notification: bool = True
    ) -> Result:
        res = await self.jsonrpc.request(
            "CopyToClipboard", [text, direct_copy, show_notification]
        )
        assert isinstance(res, Result)
        return res

    async def show_error_message(self, title: str, text: str) -> None:
        res = await self.jsonrpc.request("ShowMsgError", [title, text])
        assert isinstance(res, Result)

    async def show_message(
        self,
        title: str,
        text: str,
        icon: str = "",
        use_main_window_as_owner: bool = True,
    ) -> Result:
        res = await self.jsonrpc.request(
            "ShowMsg", [title, text, icon, use_main_window_as_owner]
        )
        assert isinstance(res, Result)
        return res

    async def open_settings_menu(self) -> None:
        res = await self.jsonrpc.request("OpenSettingDialog")
        assert isinstance(res, Result)
