from __future__ import annotations

import asyncio
import json
from typing import Any

from ..utils import MISSING
from .base_object import ToMessageBase
from .option import Option

__all__ = (
    "JsonRPCError",
    "QueryResponse",
    "ExecuteResponse",
)


class JsonRPCError(ToMessageBase):
    __slots__ = "code", "message", "data"

    def __init__(self, code: int, message: str, data: Any | None = None):
        self.code = code
        self.message = message
        self.data = data

    @classmethod
    def from_dict(cls: type[JsonRPCError], data: dict[str, Any]) -> JsonRPCError:
        return cls(code=data["code"], message=data["message"], data=data["data"])


class QueryResponse(ToMessageBase):
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


class ExecuteResponse(ToMessageBase):
    __slots__ = ("hide",)

    def __init__(self, hide: bool = True):
        self.hide = hide
