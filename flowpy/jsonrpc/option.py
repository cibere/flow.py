from __future__ import annotations

from typing import Any, Callable, Coroutine, Iterable, TypeVarTuple

from ..flow_api import FlowLauncherAPI
from ..utils import MISSING
from .base_object import Base

TS = TypeVarTuple("TS")

__all__ = (
    "Action",
    "Option",
)


class Action(Base):
    __slots__ = "method", "args"

    def __init__(
        self,
        method: Callable[[*TS], Coroutine[Any, Any, Any]],
        *args: *TS,
    ) -> None:
        parent: Any = getattr(method, "__self__", None)
        if isinstance(parent, FlowLauncherAPI):
            parameters = (method.__name__, *parameters)  # type: ignore
            method = parent.__call__  # type: ignore
        self.method = method
        self.args = args

    @property
    def name(self) -> str:
        return self.method.__qualname__

    def to_dict(self) -> dict:
        return {"method": self.name, "parameters": self.args}


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
        title_highlight_data: Iterable[int] | None = None,
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

    @classmethod
    def from_dict(cls: type[Option], data: dict[str, Any]) -> Option:
        action_data = data.get("jsonRPCAction")
        if action_data:
            action = Action.from_dict(action_data)
        else:
            action = None
        return cls(
            title=data["title"],
            sub=data.get("subTitle"),
            icon=data.get("icoPath"),
            title_highlight_data=data.get("titleHighlightData"),
            title_tooltip=data.get("titleTooltip"),
            sub_tooltip=data.get("subtitleTooltip"),
            copy_text=data.get("copyText"),
            context_data=data.get("ContextData", MISSING),
            action=action,
        )
