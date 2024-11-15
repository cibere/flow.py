from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, Awaitable, Literal

from .base import Base, add_prop

if TYPE_CHECKING:
    from .client import FlowLauncherAPI

__all__ = ("PluginMetadata",)


class PluginMetadata(Base):
    def __init__(self, data: dict[str, Any], flow_api: FlowLauncherAPI) -> None:
        super().__init__(data)
        self._flow_api = flow_api

    id: str = add_prop("id")
    name: str = add_prop("name")
    author: str = add_prop("author")
    version: str = add_prop("version")
    language: Literal[
        "csharp",
        "executable",
        "fsharp",
        "python",
        "javascript",
        "typescript",
        "python_v2",
        "executable_v2",
        "javascript_v2",
        "typescript_v2",
    ] = add_prop("language")
    description: str = add_prop("description")
    website: str = add_prop("website")
    disabled: bool = add_prop("disabled")
    directory: str = add_prop("pluginDirectory")
    keywords: list[str] = add_prop("actionKeywords")
    main_keyword: str = add_prop("actionKeyword")

    @property
    def executable(self) -> Path:
        return Path(self._data["executeFilePath"]).absolute()

    @property
    def icon(self) -> Path:
        return Path(self._data["icoPath"]).absolute()

    def add_keyword(self, keyword: str) -> Awaitable[None]:
        """
        Registers a new keyword with flow for the plugin.

        This is a shortcut to `flowpy.flow_api.FlowLauncherAPI.add_keyword`
        """

        return self._flow_api.add_keyword(self.id, keyword)

    def remove_keyword(self, keyword: str) -> Awaitable[None]:
        """
        Removes a keyword from the plugin.

        This is a shortcut to `flowpy.flow_api.FlowLauncherAPI.remove_keyword`
        """

        return self._flow_api.remove_keyword(self.id, keyword)
