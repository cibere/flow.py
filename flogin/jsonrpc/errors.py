__all__ = ("JsonRPCException", "JsonRPCVersionMismatch")


class JsonRPCException(Exception):
    r"""This is a base class which represents errors with the jsonrpc client"""


class JsonRPCVersionMismatch(JsonRPCException):
    r"""This is raised when the jsonrpc client receives a jsonrpc version which it isn't looking for

    Attributes
    --------
    expected: :class:`str`
        The Json RPC version it expected
    received: :class:`str`
        The Json RPC version it received
    """

    def __init__(self, expected: str, received: str) -> None:
        super().__init__(
            f"Expected to get version {expected}, but got {received} instead."
        )
        self.expected = expected
        self.received = received
