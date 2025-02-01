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
    font_size: int = field(default=12)
    font_family: str = field(default="sans-serif")

@dataclass
class SortOptions:
    by: str
    descending: bool = field(default=False)

@dataclass
class XOptions:
    nice: bool = field(default=True)
    grid: bool = field(default=False)
    label: str | None = field(default=None)

@dataclass
class YOptions:
    nice: bool = field(default=True)
    grid: bool = field(default=False)
    label: str | None = field(default=None)
