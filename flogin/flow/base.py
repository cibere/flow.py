from __future__ import annotations

from enum import Enum
from inspect import getmembers
from typing import Any

from ..utils import MISSING


def add_prop(
    name: str,
    *,
    default: Any = MISSING,
    cls: type[Base | Enum] = MISSING,
    is_list: bool = False,
) -> Any:
    if cls is MISSING:
        cls = lambda x: x  # type: ignore

    if cls is not MISSING and is_list is True:
        cls = lambda item: [cls(x) for x in item]  # type: ignore

    if default is MISSING:
        prop = property(lambda self: cls(self._data[name]))
    else:
        prop = property(lambda self: cls(self._data.get(name, default)))

    return prop


class Base:
    __slots__ = ("_data", "__repr_attributes__")

    def __init__(self, data: dict[str, Any]) -> None:
        self._data = data
        self.__repr_attributes__ = [
            entry[0]
            for entry in getmembers(
                self.__class__, lambda other: isinstance(other, property)
            )
        ]

    def __repr__(self) -> str:
        args = []
        for item in self.__repr_attributes__:
            args.append(f"{item}={getattr(self, item)!r}")
        return f"<{self.__class__.__name__} {' '.join(args)}>"
