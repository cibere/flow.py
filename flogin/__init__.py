__title__ = "flogin"
__author__ = "cibere"
__version__ = "0.0.4"


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


version_info: VersionInfo = VersionInfo(major=0, minor=0, micro=4, releaselevel="final")

del NamedTuple, Literal, VersionInfo
