from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from ..utils import MISSING
from .base_object import ToMessageBase

if TYPE_CHECKING:
    from .option import Option

__all__ = (
    "JsonRPCError",
    "QueryResponse",
    "ExecuteResponse",
)


class BaseResponse(ToMessageBase):
    def to_message(self, id: int) -> bytes:
        return (
            json.dumps(
                {
                    "jsonrpc": "2.0",
                    "result": self.to_dict(),
                    "id": id,
                }
            )
            + "\r\n"
        ).encode()


class JsonRPCError(BaseResponse):
    r"""This represents an error sent to or from flow.
    
    Attributes
    --------
    code: :class:`int`
        The error code for the error
    message: :class:`str`
        The error's message
    data: Optional[:class:`Any`]
        Any extra data
    """
    
    __slots__ = "code", "message", "data"

    def __init__(self, code: int, message: str, data: Any | None = None):
        self.code = code
        self.message = message
        self.data = data

    @classmethod
    def from_dict(cls: type[JsonRPCError], data: dict[str, Any]) -> JsonRPCError:
        return cls(code=data["code"], message=data["message"], data=data["data"])


class QueryResponse(BaseResponse):
    r"""This response represents the response from the `query` and `context_menu` callback methods
    
    Attributes
    --------
    options: list[:class:`Option`]
        The options to be sent as the result of the query
    settings_changes: dict[:class:`str`, Any]
        Any changes to be made to the plugin's settings.
    debug_message: :class:`str`
        A debug message if you want
    """
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


class ExecuteResponse(BaseResponse):
    r"""This response is a generic response for any callback method that isn't `query` or `context_menu`
    
    Attributes
    --------
    hide: :class:`bool`
        Whether to hide the flow menu after execution or not
    """

    __slots__ = ("hide",)

    def __init__(self, hide: bool = True):
        self.hide = hide
