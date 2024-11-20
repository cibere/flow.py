from __future__ import annotations

from typing import Any, Self

from .base_object import Base
from .errors import JsonRPCVersionMismatch

__all__ = ("Result",)


class Result(Base):
    __slots__ = "id", "data"

    def __init__(self, id: int, data: Any) -> None:
        self.id = id
        self.data = data

    @classmethod
    def from_dict(cls: type[Self], data: dict[str, Any]) -> Self:
        if data["jsonrpc"] != "2.0":
            raise JsonRPCVersionMismatch("2.0", data["jsonrpc"])

        return cls(id=data["id"], data=data["result"])
