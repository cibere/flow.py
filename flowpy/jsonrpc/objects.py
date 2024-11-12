from __future__ import annotations

import asyncio
import json

asyncio.to_thread
from typing import Any, Awaitable, Callable, Self, TypeVarTuple

from .errors import JsonRPCVersionMismatch
from .utils import MISSING

Ts = TypeVarTuple("Ts")

__all__ = (
    "Action",
    "Option",
    "JsonRPCError",
    "QueryResponse",
    "Request",
    "Result",
    "ExecuteResponse",
)


class Base:
    __slots__ = ()
    __jsonrpc_option_names__: dict[str, str] = {}

    def to_dict(self) -> dict:
        foo = {}
        for name in self.__slots__:
            item = getattr(self, name)
            if isinstance(item, Base):
                item = item.to_dict()
            elif item and isinstance(item, list) and isinstance(item[0], Base):
                item = [item.to_dict() for item in item]
            foo[self.__jsonrpc_option_names__.get(name, name)] = item
        return foo

    def _as_request(self, id: int) -> dict:
        return {
            "jsonrpc": "2.0",
            "result": self.to_dict(),
            "id": id,
        }

    def to_message(self, *, id: int = MISSING) -> bytes:
        return (
            json.dumps(self.to_dict() if id is MISSING else self._as_request(id))
            + "\r\n"
        ).encode()

    @classmethod
    def from_dict(cls: type[Self], data: dict[str, Any]) -> Self:
        raise RuntimeError("This should be overriden")

    def __repr__(self) -> str:
        args = []
        for item in self.__slots__:
            args.append(f"{item}={getattr(self, item)!r}")
        return f"<{self.__class__.__name__} {" ".join(args)}>"


class BaseResponse(Base):
    def _as_request(self, id: int) -> dict:
        return {
            "jsonrpc": "2.0",
            "result": self.to_dict(),
            "id": id,
        }

    def to_message(self, id: int) -> bytes:  # type: ignore
        return (json.dumps(self._as_request(id)) + "\r\n").encode()


class Action(Base):
    __slots__ = "id", "method", "parameters", "hide_after_finish"

    def __init__(
        self,
        id: int,
        method: Callable[[*Ts], Awaitable[Any]],
        parameters: tuple[*Ts] = MISSING,
        hide_after_finish: bool = True
    ) -> None:
        self.id = id
        self.method = method
        self.parameters = parameters or []
        self.hide_after_finish = hide_after_finish

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "method": self.method.__qualname__,
            "parameters": self.parameters,
            "DontHideAfterAction": not self.hide_after_finish
        }


class Option(Base):
    __slots__ = (
        "title",
        "sub",
        "icon",
        "title_highlight_data",
        "title_tooltip",
        "sub_tooltip",
        "copy_text",
        "action",
        "context_data",
    )

    def __init__(
        self,
        title: str,
        sub: str | None = None,
        icon: str | None = None,
        title_highlight_data: tuple[int] | None = None,
        title_tooltip: str | None = None,
        sub_tooltip: str | None = None,
        copy_text: str | None = None,
        action: Action | None = None,
        context_data: list[Any] = MISSING,
    ) -> None:
        self.title = title
        self.sub = sub
        self.icon = icon
        self.title_highlight_data = title_highlight_data
        self.title_tooltip = title_tooltip
        self.sub_tooltip = sub_tooltip
        self.copy_text = copy_text
        self.action = action
        self.context_data = context_data or []

    def to_dict(self) -> dict:
        x: dict[str, Any] = {
            "title": self.title,
        }
        if self.sub is not None:
            x["subTitle"] = self.sub
        if self.icon is not None:
            x["icoPath"] = self.icon
        if self.title_highlight_data is not None:
            x["titleHighlightData"] = self.title_highlight_data
        if self.title_tooltip is not None:
            x["titleTooltip"] = self.title_tooltip
        if self.sub_tooltip is not None:
            x["subtitleTooltip"] = self.sub_tooltip
        if self.copy_text is not None:
            x["copyText"] = self.copy_text
        if self.action is not None:
            x["jsonRPCAction"] = self.action.to_dict()
        if self.context_data is not None:
            x["ContextData"] = self.context_data
        return x


class JsonRPCError(BaseResponse):
    __slots__ = "code", "message", "data"

    def __init__(self, code: int, message: str, data: Any | None = None):
        self.code = code
        self.message = message
        self.data = data

    @classmethod
    def from_dict(cls: type[JsonRPCError], data: dict[str, Any]) -> JsonRPCError:
        return cls(code=data["code"], message=data["message"], data=data["data"])


class QueryResponse(BaseResponse):
    __slots__ = "options", "settings_changes", "debug_message"
    __jsonrpc_option_names__ = {
        "settings_changes": "settingsChanges",
        "debug_message": "debugMessage",
        "options": "result",
    }

    def __init__(
        self,
        options: list[Option],
        settings_changes: dict[str, Any] | None = None,
        debug_message: str = MISSING,
    ):
        self.options = options
        self.settings_changes = settings_changes or {}
        self.debug_message = debug_message or ""


class Request(Base):
    __slots__ = "method", "id", "params"

    def __init__(self, method: str, id: int, params: list[Any] | None = None):
        self.method = method
        self.id = id
        self.params = params

    def to_dict(self) -> dict:
        x = super().to_dict()
        x["jsonrpc"] = "2.0"
        return x


class Result(Base):
    __slots__ = "id", "data"

    def __init__(self, id: int, data: dict[str, Any]) -> None:
        self.id = id
        self.data = data

    @classmethod
    def from_dict(cls: type[Self], data: dict[str, Any]) -> Self:
        if data["jsonrpc"] != "2.0":
            raise JsonRPCVersionMismatch("2.0", data["jsonrpc"])

        return cls(id=data["id"], data=data["result"])


class ExecuteResponse(BaseResponse):
    __slots__ = ("hide",)

    def __init__(self, hide: bool = True):
        self.hide = hide
