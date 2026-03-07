from __future__ import annotations

from dataclasses import dataclass, field
from typing import overload

from .interpolations import Interpolation
from .schemes import Scheme
from .types import Index


@dataclass
class ColorOptions:
    """
    Color options applied on circles, lines, rectangles or symbols
    when it is possible.

    Attributes
    ----------
    scheme : Interpolation | Scheme
        Scheme
    """

    scheme: Interpolation | Scheme | None = field(default=None)
    legend: bool = field(default=False)
    labels: dict[int, str] | None = field(default=None)

    @classmethod
    def new(cls, values: dict | None = None) -> ColorOptions:
        default_values = ColorOptions()
        if values is None:
            return default_values
        return ColorOptions(
            scheme=values.get("scheme", default_values.scheme),
            legend=values.get("legend", default_values.legend),
            labels=values.get("labels", default_values.labels),
        )


@dataclass
class SymbolOptions:
    """
    Symbol options used for dots mark when symbols are specified.

    Attributes
    ----------
    legend : bool
        `True` if you want a legend given symbols
    """

    legend: bool = field(default=False)

    @classmethod
    def new(cls, values: dict | None = None) -> SymbolOptions:
        default_values = cls()
        if values is None:
            return default_values
        return cls(legend=values.get("legend", default_values.legend))


@dataclass
class StyleOptions:
    """
    Style options of the plot

    Attributes
    ----------
    background : str
        Background color
    color : str
        Color for text and axis
    font_size : str
        Font size of text
    font_family : str
        Font family of text
    """

    background: str = field(default="none")
    color: str = field(default="black")
    font_size: int = field(default=12)
    font_family: str = field(default="sans-serif")

    @classmethod
    def new(cls, values: dict | None = None) -> StyleOptions:
        default_values = cls()
        if values is None:
            return default_values
        return cls(
            background=values.get("background", default_values.background),
            color=values.get("color", default_values.color),
            font_size=values.get("font_size", default_values.font_size),
            font_family=values.get("font_family", default_values.font_family),
        )


@dataclass
class SortOptions:
    """
    Sort options for bar mark

    Attributes
    ----------
    by : Index | str
        Index or key value used for accessing each element in data
    descending : bool
        `True` if you want to apply descending order on data
    """

    by: Index | str = field(default="")
    descending: bool = field(default=False)

    @classmethod
    def new(cls, values: dict | None = None) -> SortOptions:
        default_values = cls()
        if values is None:
            return default_values
        return cls(
            by=values.get("by", default_values.by),
            descending=values.get("descending", default_values.descending),
        )


@dataclass
class XOptions:
    """
    Options for x axis

    Attributes
    ----------
    nice : bool
        `True` to have nicer values for x axis domain
    grid : bool
        `True` to add lines based on each x ticks
    label : str | None
        Label of the x axis
    """

    nice: bool = field(default=False)
    grid: bool = field(default=False)
    label: str | None = field(default=None)
    count: int | None = field(default=None)
    specifier: str | None = field(default=None)

    @classmethod
    def new(cls, values: dict | None = None) -> XOptions:
        default_values = cls()
        if values is None:
            return default_values
        return cls(
            nice=values.get("nice", default_values.nice),
            grid=values.get("grid", default_values.grid),
            label=values.get("label", default_values.label),
            count=values.get("count", default_values.count),
            specifier=values.get("specifier", default_values.specifier),
        )


@dataclass
class YOptions:
    """
    Options for y axis

    Attributes
    ----------
    nice : bool
        `True` to have nicer values for y axis domain
    grid : bool
        `True` to add lines based on each y ticks
    label : str | None
        Label of the y axis
    """

    nice: bool = field(default=True)
    grid: bool = field(default=False)
    label: str | None = field(default=None)
    count: int | None = field(default=None)
    specifier: str | None = field(default=None)

    @classmethod
    def new(cls, values: dict | None = None) -> YOptions:
        default_values = cls()
        if values is None:
            return default_values
        return cls(
            nice=values.get("nice", default_values.nice),
            grid=values.get("grid", default_values.grid),
            label=values.get("label", default_values.label),
            count=values.get("count", default_values.count),
            specifier=values.get("specifier", default_values.specifier),
        )


@overload
def init_options(
    values: ColorOptions | dict | None, option_class: type[ColorOptions]
): ...


@overload
def init_options(
    values: SymbolOptions | dict | None, option_class: type[SymbolOptions]
): ...


@overload
def init_options(
    values: StyleOptions | dict | None, option_class: type[StyleOptions]
): ...


@overload
def init_options(
    values: SortOptions | dict | None, option_class: type[SortOptions]
): ...


@overload
def init_options(values: XOptions | dict | None, option_class: type[XOptions]): ...


@overload
def init_options(values: YOptions | dict | None, option_class: type[YOptions]): ...


def init_options(values, option_class):
    """
    Initialize an option class from dictionary values

    Parameters
    ----------
    values : T | dict | None
        Dictionary option values
    option_class : type[T]
        Option class

    Returns
    -------
    T
        Instance of the option class
    """
    return values if isinstance(values, option_class) else option_class.new(values)
