from abc import ABC, abstractmethod

from detroit.selection import Selection

from ..context import Context
from ..scaler import Scaler
from ..types import Number


class Mark(ABC):
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
    y_domain : tuple[Number, Number] | list[str] | None
        Domain for y axis described as (min, max) values or a list of string values.
    x_scaler_type : TScaler | None
        Scaler type for x axis of the mark.
    y_scaler_type : TScaler | None
        Scaler type for x axis of the mark.
    _context : MarkContext | None
        Context of the mark which holds dimensions and color scheme
    """

    def __init__(self):
        self.x_label: str | None = None
        self.y_label: str | None = None
        self.x_domain: tuple[Number, Number] | list[str] | None = None
        self.y_domain: tuple[Number, Number] | list[str] | None = None
        self.x_scaler_type: Scaler | None = None
        self.y_scaler_type: Scaler | None = None

    @abstractmethod
    def apply(self, svg: Selection, ctx: Context):
        """
        Method which is called by `plot` and which should change `svg` content.

        Parameters
        ----------
        svg : Selection
            SVG content defined by a `Selection` class from `detroit`
        ctx : Context
            SVG context containing shared data between marks
        """
        ...
