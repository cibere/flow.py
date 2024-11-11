__all__ = ("JsonRPCException", "JsonRPCVersionMismatch")


class JsonRPCException(Exception): ...


class JsonRPCVersionMismatch(JsonRPCException):
    def __init__(self, expected: str, received: str) -> None:
        super().__init__(
            f"Expected to get version {expected}, but got {received} instead."
        )
        self.expected = expected
        self.received = received
