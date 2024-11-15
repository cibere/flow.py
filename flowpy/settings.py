from __future__ import annotations

from typing import Any

from .errors import SettingNotFound

__all__ = ("Settings",)

type RawSettings = dict[str, Any]


class Settings:
    _data: RawSettings
    _changes: RawSettings

    def __init__(self, data: RawSettings) -> None:
        self._data = data
        self._changes = {}

    def __getitem__(self, key: str) -> Any:
        try:
            return self._data[key]
        except KeyError:
            raise SettingNotFound(key) from None

    def __setitem__(self, key: str, value: Any) -> None:
        self._data[key] = value
        self._changes[key] = value

    def __getattribute__(self, name: str) -> Any:
        if name.startswith("_"):
            try:
                return super().__getattribute__(name)
            except AttributeError as e:
                raise AttributeError(
                    f"{e}. Settings that start with an underscore (_) can only be accessed by the __getitem__ method. Ex: settings['_key']"
                ) from None
        return self.__getitem__(name)

    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith("_"):
            return super().__setattr__(name, value)
        self.__setitem__(name, value)
