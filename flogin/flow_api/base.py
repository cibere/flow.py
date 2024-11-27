from inspect import getmembers
from typing import Any


def add_prop(name: str) -> Any:
    return property(lambda self: self._data[name])


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
