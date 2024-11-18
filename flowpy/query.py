from typing import Any

__all__ = ("Query",)


class Query:
    r"""This class represents the query data sent from flow launcher
    """

    def __init__(self, data: dict[str, Any]) -> None:
        self.__data = data

    @property
    def raw_text(self) -> str:
        """:class:`str`: The raw and complete query, which includes the keyword"""
        return self.__data["rawQuery"]

    @property
    def is_requery(self) -> bool:
        """:class:`bool`: Whether the query is a requery or not"""
        return self.__data["isReQuery"]

    @property
    def text(self) -> str:
        """:class:`str`: The actual query, excluding any keywords"""
        return self.__data["search"]

    @property
    def keyword(self) -> str:
        """:class:`str`: The keyword used to initiate the query"""
        return self.__data["actionKeyword"]
