__title__ = "flow.py"
__author__ = "cibere"
__version__ = "0.0.1a"


from typing import Literal, NamedTuple

from .conditions import *
from .errors import *
from .jsonrpc import *
from .plugin import *
from .query import *
from .search_handler import *
from .settings import *


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]


version_info: VersionInfo = VersionInfo(major=0, minor=0, micro=1, releaselevel="alpha")

del NamedTuple, Literal, VersionInfo
