from __future__ import annotations

import logging
import random
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Coroutine,
    Iterable,
    NotRequired,
    Self,
    TypedDict,
    TypeVarTuple,
    Unpack,
)

from ..utils import cached_property, copy_doc
from .base_object import Base
from .responses import ErrorResponse

if TYPE_CHECKING:
    from .._types import SearchHandlerCallbackReturns
    from ..plugin import Plugin
    from .responses import ExecuteResponse

TS = TypeVarTuple("TS")
LOG = logging.getLogger(__name__)

__all__ = ("Result",)


class ResultConstructorArgs(TypedDict):
    title: str
    sub: NotRequired[str | None]
    icon: NotRequired[str | None]
    title_highlight_data: NotRequired[Iterable[int] | None]
    title_tooltip: NotRequired[str | None]
    sub_tooltip: NotRequired[str | None]
    copy_text: NotRequired[str | None]
    score: NotRequired[int | None]


class Result(Base):
    r"""This represents a result that would be returned as a result for a query or context menu.

    For simple useage: create instances of this class as-is.

    For advanced useage (handling clicks and custom context menus), it is recommended to subclass the result object to create your own subclass.

    Subclassing
    ------------
    Subclassing lets you override the following methods: :func:`~flogin.jsonrpc.results.Result.callback` and :func:`~flogin.jsonrpc.results.Result.context_menu`. It also lets you create "universal" result properties (eg: same icon). Example:

    .. code-block:: python3

        class MyResult(Result):
            def __init__(self, title: str) -> None:
                super().__init__(self, title, icon="Images/app.png")

            async def callback(self):
                # handle what happens when the result gets clicked

            async def context_menu(self):
                # add context menu options to this result's context menu

    Attributes
    ----------
    title: :class:`str`
        The title/content of the result
    sub: Optional[:class:`str`]
        The subtitle to be shown.
    icon: Optional[:class:`str`]
        A path to the icon to be shown with the result.
    title_highlight_data: Optional[Iterable[:class:`int`]]
        The highlight data for the title. See the :ref:`FAQ section on highlights <highlights>` for more info.
    title_tooltip: Optional[:class:`str`]
        The text to be displayed when the user hovers over the result's title
    sub_tooltip: Optional[:class:`str`]
        The text to be displayed when the user hovers over the result's subtitle
    copy_text: Optional[:class:`str`]
        This is the text that will be copied when the user does ``CTRL+C`` on the result.
    plugin: :class:`~flogin.plugin.Plugin` | None
        Your plugin instance. This is filled before :func:`~flogin.jsonrpc.results.Result.callback` or :func:`~flogin.jsonrpc.results.Result.context_menu` are triggered.
    """

    def __init__(
        self,
        title: str,
        sub: str | None = None,
        icon: str | None = None,
        title_highlight_data: Iterable[int] | None = None,
        title_tooltip: str | None = None,
        sub_tooltip: str | None = None,
        copy_text: str | None = None,
        score: int | None = None,
    ) -> None:
        self.title = title
        self.sub = sub
        self.icon = icon
        self.title_highlight_data = title_highlight_data
        self.title_tooltip = title_tooltip
        self.sub_tooltip = sub_tooltip
        self.copy_text = copy_text
        self.score = score
        self.plugin: Plugin | None = None

    async def on_error(self, error: Exception) -> ErrorResponse | ExecuteResponse:
        r"""|coro|

        Override this function to add an error response behavior to this result's callback.

        Parameters
        ----------
        error: :class:`Exception`
            The error that occured
        """
        LOG.exception(
            f"Ignoring exception in reuslt callback ({self!r})", exc_info=error
        )
        return ErrorResponse.internal_error(error)

    async def callback(self) -> ExecuteResponse:
        r"""|coro|

        Override this function to add a callback behavior to your result. This method will run when the user clicks on your result.

        Returns
        -------
        :class:`~flogin.jsonrpc.responses.ExecuteResponse`
            A response to flow determining whether or not to hide flow's menu
        """

        return ExecuteResponse(False)

    def context_menu(self) -> SearchHandlerCallbackReturns:
        r"""|coro|

        Override this function to add a context menu behavior to your result. This method will run when the user gets the context menu to your result.

        This method can return/yield almost anything, and flogin will convert it into a list of :class:`~flogin.jsonrpc.results.Result` objects before sending it to flow.

        Returns
        -------
        list[:class:`~flogin.jsonrpc.results.Result`] | :class:`~flogin.jsonrpc.results.Result` | str | Any
            A list of results, an results, or something that can be converted into a list of results.

        Yields
        ------
        :class:`~flogin.jsonrpc.results.Result` | str | Any
            A result object or something that can be converted into a result object.
        """
        ...

    def on_context_menu_error(
        self, error: Exception
    ) -> SearchHandlerCallbackReturns:
        r"""|coro|

        Override this function to add an error response behavior to this result's context menu callback.

        If the error was handled:
            You can return/yield almost anything, and flogin will convert it into a list of :class:`~flogin.jsonrpc.results.Result` objects before sending it to flow.

        If the error was not handled:
            Return a :class:`~flogin.jsonrpc.responses.ErrorResponse` object

        Parameters
        ----------
        error: :class:`Exception`
            The error that occured

        Returns
        -------
        :class:`~flogin.jsonrpc.responses.ErrorResponse` | list[:class:`~flogin.jsonrpc.results.Result`] | :class:`~flogin.jsonrpc.results.Result` | str | Any
            A list of results, an results, or something that can be converted into a list of results.

        Yields
        ------
        :class:`~flogin.jsonrpc.results.Result` | str | Any
            A result object or something that can be converted into a result object.
        """
        ...

    if not TYPE_CHECKING:
        
        @copy_doc(context_menu)
        async def context_menu(self):
            return []

        @copy_doc(on_context_menu_error)
        async def on_context_menu_error(self, error: Exception):
            LOG.exception(
                f"Ignoring exception in result's context menu callback ({self!r})",
                exc_info=error,
            )
            return ErrorResponse.internal_error(error)

    def to_dict(self) -> dict[str, Any]:
        r"""This converts the result into a json serializable dictionary

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
        if self.callback is not None:
            x["jsonRPCAction"] = {"method": f"flogin.action.{self.slug}"}
        if self.context_menu is not None:
            x["ContextData"] = [self.slug]
        if self.score is not None:
            x["score"] = self.score
        return x

    @classmethod
    def from_dict(cls: type[Self], data: dict[str, Any]) -> Self:
        r"""Creates a Result from a dictionary

        .. NOTE::
            This method does NOT fill the :func:`~flogin.jsonrpc.results.Result.callback` or :func:`~flogin.jsonrpc.results.Result.context_menu` attributes.

        Parameters
        ----------
        data: dict[:class:`str`, Any]
            The valid dictionary that includes the result data

        Raises
        ------
        :class:`KeyError`
            The dictionary did not include the only required field, ``title``.

        Returns
        --------
        :class:`Result`
        """

        return cls(
            title=data["title"],
            sub=data.get("subTitle"),
            icon=data.get("icoPath"),
            title_highlight_data=data.get("titleHighlightData"),
            title_tooltip=data.get("titleTooltip"),
            sub_tooltip=data.get("subtitleTooltip"),
            copy_text=data.get("copyText"),
        )

    @classmethod
    def from_anything(cls: type[Result], item: Any) -> Result:
        if isinstance(item, dict):
            return cls.from_dict(item)
        elif isinstance(item, Result):
            return item
        else:
            return cls(str(item))

    @classmethod
    def create_with_partial(
        cls: type[Result],
        partial_callback: Callable[[], Coroutine[Any, Any, Any]],
        **kwargs: Unpack[ResultConstructorArgs],
    ) -> Result:
        r"""A quick and easy way to create a result with a callback without subclassing.

        .. NOTE::
            This is meant to be used with :class:`~flogin.flow_api.client.FlowLauncherAPI` methods

        Example
        --------
        .. code-block:: python3

            result = Result.create_with_partial(
                functools.partial(
                    plugin.api.show_notification,
                    "notification title",
                    "notification content"
                ),
                title="Result title",
                sub="Result subtitle"
            )

        Parameters
        ----------
        partial_callback: partial :ref:`coroutine <coroutine>`
            The callback wrapped in :obj:`functools.partial`
        kwargs: See allowed kwargs here: :class:`~flogin.jsonrpc.results.Result`
            The args that will be passed to the :class:`~flogin.jsonrpc.results.Result` constructor
        """

        self = cls(**kwargs)
        self.callback = partial_callback
        return self

    @cached_property
    def slug(self) -> str:
        return "".join(
            random.choices(
                "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890", k=15
            )
        )
