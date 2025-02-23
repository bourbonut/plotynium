from typing import TypeVar, TypeAlias, Protocol
from collections.abc import Callable
from detroit.selection.selection import Selection

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")
Number: TypeAlias = int | float
Data: TypeAlias = Number | str
Index: TypeAlias = int

TScaler = TypeVar("TScaler", bound="Scaler")

class Mark(Protocol):
    x_label: str | None
    y_label: str | None
    x_domain: tuple[Number, Number] | list[str] | None
    y_domain: tuple[Number, Number] | None
    x_scaler_type: TScaler | None
    y_scaler_type: TScaler | None

    def __call__(self, svg: Selection, x: Callable, y: Callable, **kwargs):
        ...
