__title__ = "flow.py"
__author__ = "cibere"
__version__ = "0.0.1"


from typing import Literal, NamedTuple

from .conditions import *
from .context_menu_handler import *
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
    serial: int


version_info: VersionInfo = VersionInfo(
    major=2, minor=5, micro=0, releaselevel="alpha", serial=0
)

del NamedTuple, Literal, VersionInfo
