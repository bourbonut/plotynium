from typing import TypeVar, TypeAlias, Protocol
from collections.abc import Callable
from detroit.selection import Selection

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")
Number: TypeAlias = int | float
Data: TypeAlias = Number | str
Index: TypeAlias = int

TScaler = TypeVar("TScaler", bound="Scaler")

class Mark(Protocol):
    """
    Description of what should be a `Mark`. Since `plot` takes a list of marks, its
    attributes will be mixed with other marks in order to generate a plot with single
    characteristics such as label values, domain values and scaler types.

    Attributes
    ----------
    x_label : str | None
        Label for x axis.
    y_label : str | None
        Label for y axis.
    x_domain : tuple[Number, Number] | list[str] | None
        Domain for x axis described as (min, max) values or a list of string values.
    y_domain : tuple[Number, Number] | None
        Domain for y axis described as (min, max) values or a list of string values.
    x_scaler_type : TScaler | None
        Scaler type for x axis of the mark.
    y_scaler_type : TScaler | None
        Scaler type for x axis of the mark.
    legend_labels : list[str | int] | None
        Labels used for legend of the mark.
    """
    x_label: str | None
    y_label: str | None
    x_domain: tuple[Number, Number] | list[str] | None
    y_domain: tuple[Number, Number] | None
    x_scaler_type: TScaler | None
    y_scaler_type: TScaler | None
    legend_labels: list[str | int] | None

    def __call__(self, svg: Selection, x: Callable, y: Callable, **kwargs):
        """
        Method which is called by `plot` and which should change `svg` content.

        Parameters
        ----------
        svg : Selection
            SVG content defined by a `Selection` class from `detroit`
        x : Callable
            This argument is a scaler for x axis which behaves like a function. By
            passing a data, it returns the x position on the plot.
        y : Callable
            This argument is a scaler for y axis which behaves like a function. By
            passing a data, it returns the y position on the plot.
        """
        ...
