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
    """This represents a |coroutine_link|_ that will be triggered when a user clicks on an option.
    
    Attributes
    ----------
    method: :ref:`coroutine <coroutine>`
        The |coroutine|_ that will be ran when the user clicks the option this is associated with
    args: Iterable[Any]
        The arguments that will be passed to the coroutine
    """

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
        """:class:`str`: The name of the method provided"""
        return self.method.__qualname__

    def to_dict(self) -> dict:
        """This converts the action into a json serializable dictionary
        
        Returns
        -------
        :class:`dict`[:class:`str`, Any]
        """

        return {"method": self.name, "parameters": self.args}


class Option(Base):
    """This represents an option that would be returned as a result for a query or context menu.
    
    Attributes
    ----------
    title: :class:`str`
        The title/content of the option
    sub: Optional[:class:`str`]
        The subtitle to be shown.
    icon: Optional[:class:`str`]
        A path to the icon to be shown with the option.
    title_highlight_data: Optional[:class:`Iterable`[:class:`int`]]
        The highlight data for the title. See the `FAQ section on highlights <highlights>` for more info.
    title_tooltip: Optional[:class:`str`]
        The text to be displayed when the user hovers over the option's title
    sub_tooltip: Optional[:class:`str`]
        The text to be displayed when the user hovers over the option's subtitle
    copy_text: Optional[:class:`str`]
        I have no idea
    action: Optional[:class:`Action`]
        The action to be preformed when the user clicks on the option
    context_data: Optional[:class:`Iterable`[Any]]
        A list of json seriable objects which will be given in the `on_context_menu event <on_context_menu>` when the user requests the context menu for this option.
    """

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

    def to_dict(self) -> dict[str, Any]:
        r"""This converts the option into a json serializable dictionary
        
        Returns
        -------
        :class:`dict`[:class:`str`, Any]
        """

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
        """Creates an Option from a dictionary
        
        Parameters
        ----------
        data: :class:`dict`[:class:`str`, Any]
            The valid dictionary that includes the option data
        
        Raises
        ------
        :class:`KeyError`
            The dictionary did not include the only required field, ``title``.
        
        Returns
        --------
        :class:`Option`
        """

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
