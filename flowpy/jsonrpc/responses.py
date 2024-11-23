from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from ..utils import MISSING
from .base_object import ToMessageBase

if TYPE_CHECKING:
    from .client import JsonRPCClient
    from .option import Option

__all__ = (
    "ErrorResponse",
    "QueryResponse",
    "ExecuteResponse",
)


class BaseResponse(ToMessageBase):
    r"""This represents a response to flow.

    .. WARNING::
        This class is NOT to be used as is. Use one of it's subclasses instead.
    """

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

    def prepare(self, client: JsonRPCClient) -> None: ...


class ErrorResponse(BaseResponse):
    r"""This represents an error sent to or from flow.

    Attributes
    --------
    code: :class:`int`
        The error code for the error
    message: :class:`str`
        The error's message
    data: Optional[Any]
        Any extra data
    """

    __slots__ = "code", "message", "data"

    def __init__(self, code: int, message: str, data: Any | None = None):
        self.code = code
        self.message = message
        self.data = data

    def to_dict(self) -> dict:
        data = self.data
        if isinstance(data, Exception):
            data = f"{data}"
        return {"code": self.code, "message": self.message, "data": data}

    @classmethod
    def from_dict(cls: type[ErrorResponse], data: dict[str, Any]) -> ErrorResponse:
        return cls(code=data["code"], message=data["message"], data=data["data"])

    @classmethod
    def internal_error(cls: type[ErrorResponse], data: Any = None) -> ErrorResponse:
        return cls(code=-32603, message="Internal error", data=data)


class QueryResponse(BaseResponse):
    r"""This response represents the response from the :ref:`on_query <on_query>` and :ref:`on_context_menu <on_context_menu>` events.

    Attributes
    --------
    options: list[:class:`~flowpy.jsonrpc.option.Option`]
        The options to be sent as the result of the query
    settings_changes: dict[:class:`str`, Any]
        Any changes to be made to the plugin's settings.
    debug_message: :class:`str`
        A debug message if you want
    """

    __slots__ = "options", "settings_changes", "debug_message"
    __jsonrpc_option_names__ = {
        "settings_changes": "SettingsChange",
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

    def prepare(self, client: JsonRPCClient) -> None:
        for opt in self.options:
            if opt.action:
                client.action_callback_mapping[opt.action.name] = opt.action.method


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
