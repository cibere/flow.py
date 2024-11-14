from __future__ import annotations

from typing import TYPE_CHECKING, Any, ParamSpec

from .fuzzy_search import FuzzySearchResult

ATS = ParamSpec("ATS")

if TYPE_CHECKING:
    from ..jsonrpc import ExecuteResponse, JsonRPCClient, Result

__all__ = ("FlowLauncherAPI",)


class FlowLauncherAPI:
    def __init__(self, jsonrpc: JsonRPCClient):
        self.jsonrpc = jsonrpc

    async def __call__(self, method: str, *args: Any, **kwargs: Any) -> ExecuteResponse:
        from ..jsonrpc import ExecuteResponse

        await getattr(self, method)(*args, **kwargs)
        return ExecuteResponse()

    async def fuzzy_search(
        self, text: str, text_to_compare_it_to: str
    ) -> FuzzySearchResult:
        from ..jsonrpc import Result  # circular import

        res = await self.jsonrpc.request("FuzzySearch", [text, text_to_compare_it_to])
        assert isinstance(res, Result)
        return FuzzySearchResult(res.data)

    async def change_query(self, new_query: str, requery: bool = False) -> None:
        from ..jsonrpc import Result  # circular import

        res = await self.jsonrpc.request("ChangeQuery", [new_query, requery])
        assert isinstance(res, Result)

    async def copy_to_clipboard(
        self, text: str, direct_copy: bool = False, show_notification: bool = True
    ) -> Result:
        from ..jsonrpc import Result  # circular import

        res = await self.jsonrpc.request(
            "CopyToClipboard", [text, direct_copy, show_notification]
        )
        assert isinstance(res, Result)
        return res

    async def show_error_message(self, title: str, text: str) -> None:
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
        from ..jsonrpc import Result  # circular import

        res = await self.jsonrpc.request(
            "ShowMsg", [title, text, icon, use_main_window_as_owner]
        )
        assert isinstance(res, Result)
        return res

    async def open_settings_menu(self) -> None:
        from ..jsonrpc import Result  # circular import

        res = await self.jsonrpc.request("OpenSettingDialog")
        assert isinstance(res, Result)

    async def open_url(self, url: str, in_private: bool) -> None:
        from ..jsonrpc import Result  # circular import

        res = await self.jsonrpc.request("OpenUrl", [url, in_private])
        assert isinstance(res, Result)
