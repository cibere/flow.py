from typing import Any

__all__ = ("Query",)


class Query:
    def __init__(self, data: dict[str, Any]) -> None:
        self.__data = data

    @property
    def raw_text(self) -> str:
        return self.__data["rawQuery"]

    @property
    def is_requery(self) -> bool:
        return self.__data["isReQuery"]

    @property
    def text(self) -> str:
        return self.__data["search"]

    @property
    def keyword(self) -> str:
        return self.__data["actionKeyword"]
