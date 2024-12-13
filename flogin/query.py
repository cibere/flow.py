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

    Attributes
    ----------
    raw_text: :class:`str`:
        The raw and complete query, which includes the keyword
    is_requery: :class:`bool`
        Whether the query is a requery or not
    text: :class:`str`
        The actual query, excluding any keywords
    keyword: :class:`str`
        The keyword used to initiate the query
    """

    def __init__(
        self, *, raw_text: str, is_requery: bool = False, text: str, keyword: str
    ) -> None:
        self.__search_condition_data: T | None = None

        self.raw_text = raw_text
        self.is_requery = is_requery
        self.text = text
        self.keyword = keyword

    @classmethod
    def from_json(cls: type[Query], data: dict[str, Any]) -> Query:
        return cls(
            raw_text=data["rawQuery"],
            is_requery=data["isReQuery"],
            text=data["search"],
            keyword=data["actionKeyword"],
        )

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

    def __repr__(self) -> str:
        return f"<Query {self.raw_text=} {self.text=} {self.keyword=} {self.is_requery=} {self.condition_data=}>"
