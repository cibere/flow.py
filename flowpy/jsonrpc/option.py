from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Coroutine, Iterable, TypeVarTuple

from ..flow_api import FlowLauncherAPI
from .base_object import Base

if TYPE_CHECKING:
    from ..context_menu_handler import ContextMenuHandler
    from .responses import ExecuteResponse

TS = TypeVarTuple("TS")

__all__ = (
    "Action",
    "Option",
)


class Action(Base):
    r"""This represents a :ref:`coroutine <coroutine>` that will be triggered when a user clicks on an option.

    .. NOTE::
        See the :func:`~flowpy.plugin.Plugin.action` decorator for an alternate way of creating actions

    Attributes
    ----------
    method: :ref:`coroutine <coroutine>`
        The :ref:`coroutine <coroutine>` that will be ran when the user clicks the option this is associated with
    args: Iterable[Any]
        The arguments that will be passed to the coroutine
    """

    __slots__ = "method", "args"

    def __init__(
        self,
        method: Callable[[*TS], Coroutine[Any, Any, ExecuteResponse]],
        *args: *TS,
    ) -> None:
        parent: Any = getattr(method, "__self__", None)
        if isinstance(parent, FlowLauncherAPI):
            parameters = (method.__name__, *args)  # type: ignore
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
        dict[:class:`str`, Any]
        """

        return {"method": self.name, "parameters": self.args}


class Option(Base):
    r"""This represents an option that would be returned as a result for a query or context menu.

    Attributes
    ----------
    title: :class:`str`
        The title/content of the option
    sub: Optional[:class:`str`]
        The subtitle to be shown.
    icon: Optional[:class:`str`]
        A path to the icon to be shown with the option.
    title_highlight_data: Optional[Iterable[:class:`int`]]
        The highlight data for the title. See the :ref:`FAQ section on highlights <highlights>` for more info.
    title_tooltip: Optional[:class:`str`]
        The text to be displayed when the user hovers over the option's title
    sub_tooltip: Optional[:class:`str`]
        The text to be displayed when the user hovers over the option's subtitle
    copy_text: Optional[:class:`str`]
        This is the text that will be copied when the user does `CTRL+C` on the option.
    action: Optional[:class:`Action`]
        The action to be preformed when the user clicks on the option
    context_menu_handler: Optional[:class:`~flowpy.context_menu_handler.ContextMenuHandler`]
        The context menu handler to create the context menu for this option. See the :ref:`context menu handler section <ctx_menu_handlers>` for more information about using context menu handlers.
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
        "context_menu_handler",
        "score",
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
        context_menu_handler: ContextMenuHandler | None = None,
        score: int | None = None,
    ) -> None:
        self.title = title
        self.sub = sub
        self.icon = icon
        self.title_highlight_data = title_highlight_data
        self.title_tooltip = title_tooltip
        self.sub_tooltip = sub_tooltip
        self.copy_text = copy_text
        self.action = action
        self.score = score
        self.context_menu_handler = context_menu_handler

    def to_dict(self) -> dict[str, Any]:
        r"""This converts the option into a json serializable dictionary

        Returns
        -------
        dict[:class:`str`, Any]
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
        if self.context_menu_handler is not None:
            x["ContextData"] = [self.context_menu_handler.slug]
        if self.score is not None:
            x["score"] = self.score
        return x

    @classmethod
    def from_dict(cls: type[Option], data: dict[str, Any]) -> Option:
        r"""Creates an Option from a dictionary

        .. NOTE::
            This method does NOT fill the :attr:`~flowpy.jsonrpc.option.Option.context_menu_handler` attribute.

        Parameters
        ----------
        data: dict[:class:`str`, Any]
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
            action=action,
        )

    @classmethod
    def from_anything(cls: type[Option], item: Any) -> Option:
        if isinstance(item, dict):
            return cls.from_dict(item)
        elif isinstance(item, Option):
            return item
        else:
            return cls(str(item))
