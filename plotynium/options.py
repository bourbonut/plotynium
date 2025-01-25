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
