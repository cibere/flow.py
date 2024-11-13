from .base import Base, add_prop

__all__ = ("FuzzySearchResult",)


class FuzzySearchResult(Base):
    score: int = add_prop("score")
    match_data: list[int] = add_prop("matchData")
    search_precision: int = add_prop("searchPrecision")
