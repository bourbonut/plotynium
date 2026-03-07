from datetime import datetime
from typing import Any, TypeAlias, TypeVar

from .interpolations import Interpolation
from .schemes import Scheme

T = TypeVar("T", bound=Any)
U = TypeVar("U")
V = TypeVar("V")
Number: TypeAlias = int | float
Data: TypeAlias = Number | str | datetime
Index: TypeAlias = int
ColorScheme: TypeAlias = Scheme | Interpolation
