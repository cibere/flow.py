from __future__ import annotations

from typing import Any, Generic, TypeVar

T = TypeVar("T")

__all__ = ("Query",)


class Query(Generic[T]):
    r"""This class represents the query data sent from flow launcher

    .. container:: operations

        .. describe:: x == y

            Compare the keywords, text, and is_query values of two query objects.

        .. describe:: hash(x)

            Gets the hash of the query's raw text
    """

    def __init__(self, data: dict[str, Any]) -> None:
        self.__data = data
        self.__search_condition_data: T | None = None

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

    @property
    def condition_data(self) -> T | None:
        """Any | None: If used in a :class:`~flogin.search_handler.SearchHandler`, this attribute will return any extra data that the condition gave."""
        return self.__search_condition_data

    @condition_data.setter
    def condition_data(self, value: T) -> None:
        self.__search_condition_data = value

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, Query)
            and other.raw_text == self.raw_text
            and other.is_requery == self.is_requery
        )

    def __hash__(self) -> int:
        return hash(self.raw_text)
