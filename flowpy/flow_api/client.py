from ..jsonrpc import JsonRPCClient, Result

from .fuzzy_search import FuzzySearchResult

class FlowLauncherAPI:
    def __init__(self, jsonrpc: JsonRPCClient):
        self.jsonrpc = jsonrpc
    
    async def fuzzy_search(self, text: str, text_to_compare_it_to: str) -> FuzzySearchResult:
        res = await self.jsonrpc.request("FuzzySearch", [text, text_to_compare_it_to])
        assert isinstance(res, Result)
        return FuzzySearchResult(res.data)
    
    async def change_query(self, new_query: str, requery: bool = False) -> None:
        res = await self.jsonrpc.request("ChangeQuery", [new_query, requery])
        assert isinstance(res, Result)
    
    async def copy_to_clipboard(self, text: str, direct_copy: bool = False, show_notification: bool = True) -> Result:
        res = await self.jsonrpc.request("CopyToClipboard", [text, direct_copy, show_notification])
        assert isinstance(res, Result)
        return res
    
    async def show_error_message(self, title: str, subtitle: str) -> None:
        res = await self.jsonrpc.request("ShowMsgError", [title, subtitle])
        assert isinstance(res, Result)
    
    """async def show_message(self, title: str, subtitle: str = "", icon: str = "") -> Result:
        res = await self.jsonrpc.request("ShowMsgError", [title, subtitle, icon])
        assert isinstance(res, Result)
        return res"""
    
    async def open_settings_menu(self) -> None:
        res = await self.jsonrpc.request("OpenSettingDialog")
        assert isinstance(res, Result)