from typing import TypeAlias, TypeVar

from .interpolations import Interpolation
from .schemes import Scheme

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")
Number: TypeAlias = int | float
Data: TypeAlias = Number | str
Index: TypeAlias = int
ColorScheme: TypeAlias = Scheme | Interpolation
