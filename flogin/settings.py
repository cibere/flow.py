from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .errors import SettingNotFound

if TYPE_CHECKING:
    from ._types import RawSettings

__all__ = ("Settings",)


class Settings:
    r"""This class represents the settings that you user has chosen

    .. container:: operations

        .. describe:: x['setting name']

            Get a setting by key similiar to a dictionary

        .. describe:: x['setting name'] = "new value"

            Change a settings value like a dictionary

        .. describe:: x.setting_name

            Get a setting by name like an attribute

        .. describe:: x.setting_name = "new value"

            Change a settings value like an attribute


    Raises
    --------
    :class:`SettingNotFound`
        A setting was not found
    """

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

    def _update(self, data: RawSettings) -> None:
        self._data = data
        self._changes = {}

    def __repr__(self) -> str:
        return f"<Settings current={self._data!r}, pending_changes={self._changes}>"
