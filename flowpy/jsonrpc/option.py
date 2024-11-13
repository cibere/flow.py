from __future__ import annotations

from typing import Any, Awaitable, Callable, TypeVarTuple

from .base_object import Base
from .utils import MISSING

Ts = TypeVarTuple("Ts")

__all__ = (
    "Action",
    "Option",
)


class Action(Base):
    __slots__ = "method", "parameters", "hide_after_finish", "__id"

    def __init__(
        self,
        method: Callable[[*Ts], Awaitable[Any]],
        parameters: tuple[*Ts] = MISSING,
        hide_after_finish: bool = True,
    ) -> None:
        self.method = method
        self.parameters = parameters or []
        self.hide_after_finish = hide_after_finish
        self.__id: int | None = None

    @property
    def id(self) -> int:
        if self.__id is None:
            raise RuntimeError("Action has not been assigned and id")
        else:
            return self.__id

    @id.setter
    def id(self, value: int) -> None:
        self.__id = value

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "method": self.method.__qualname__,
            "parameters": self.parameters,
            "DontHideAfterAction": not self.hide_after_finish,
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
