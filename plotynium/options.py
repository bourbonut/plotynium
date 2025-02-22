from dataclasses import dataclass, field
from .schemes import Scheme
from .interpolations import Interpolation
from typing import TypeVar

T = TypeVar("T")

@dataclass
class ColorOptions:
    scheme: Interpolation | Scheme = field(default=Interpolation.TURBO)

    @staticmethod
    def new(values: dict | None = None):
        default_values = ColorOptions()
        if values is None:
            return default_values
        return ColorOptions(
            scheme=values.get("scheme", default_values.scheme)
        )

@dataclass
class SymbolOptions:
    legend: bool = field(default=False)

    @staticmethod
    def new(values: dict | None = None):
        default_values = SymbolOptions()
        if values is None:
            return default_values
        return SymbolOptions(
            legend=values.get("legend", default_values.legend)
        )

@dataclass
class StyleOptions:
    background: str = field(default="none")
    color: str = field(default="black")
    font_size: int = field(default=12)
    font_family: str = field(default="sans-serif")

    @staticmethod
    def new(values: dict | None = None):
        default_values = StyleOptions()
        if values is None:
            return default_values
        return StyleOptions(
            background=values.get("background", default_values.background),
            color=values.get("color", default_values.color),
            font_size=values.get("font_size", default_values.font_size),
            font_family=values.get("font_family", default_values.font_family),
        )

@dataclass
class SortOptions:
    by: str = field(default="")
    descending: bool = field(default=False)

    @staticmethod
    def new(values: dict | None = None):
        default_values = SortOptions()
        if values is None:
            return default_values
        return SortOptions(
            by=values.get("by", default_values.by),
            descending=values.get("descending", default_values.descending),
        )

@dataclass
class XOptions:
    nice: bool = field(default=False)
    grid: bool = field(default=False)
    label: str | None = field(default=None)

    @staticmethod
    def new(values: dict | None = None):
        default_values = XOptions()
        if values is None:
            return default_values
        return XOptions(
            nice=values.get("nice", default_values.nice),
            grid=values.get("grid", default_values.grid),
            label=values.get("label", default_values.label),
        )

@dataclass
class YOptions:
    nice: bool = field(default=False)
    grid: bool = field(default=False)
    label: str | None = field(default=None)

    @staticmethod
    def new(values: dict | None = None):
        default_values = YOptions()
        if values is None:
            return default_values
        return YOptions(
            nice=values.get("nice", default_values.nice),
            grid=values.get("grid", default_values.grid),
            label=values.get("label", default_values.label),
        )

def init_options(values: T | dict | None, option_class: type[T]) -> T:
    return values if isinstance(values, option_class) else option_class.new(values)
