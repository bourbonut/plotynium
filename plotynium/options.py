from dataclasses import dataclass, field
from .schemes import Scheme

@dataclass
class ColorOptions:
    scheme: Scheme = field(default=Scheme.TURBO)

@dataclass
class SymbolOptions:
    legend: bool = field(default=False)

@dataclass
class StyleOptions:
    background: str = field(default="none")
    color: str = field(default="black")

@dataclass
class SortOptions:
    by: str
    descending: bool = field(default=False)

@dataclass
class XOptions:
    grid: bool = field(default=False)
    label: str | None = field(default=None)

@dataclass
class YOptions:
    grid: bool = field(default=False)
    label: str | None = field(default=None)
