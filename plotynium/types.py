from .interpolations import Interpolation
from .schemes import Scheme
from typing import TypeVar, TypeAlias

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")
Number: TypeAlias = int | float
Data: TypeAlias = Number | str
Index: TypeAlias = int
ColorScheme: TypeAlias = Scheme | Interpolation
