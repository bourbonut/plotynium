from dataclasses import dataclass, field
from collections import OrderedDict
from .types import ColorScheme
from detroit.types import Scaler

__all__ = ["Context"]

@dataclass
class Context:
    """

    Parameters
    ----------
    x : Scaler
        This argument is a scaler for x axis which behaves like a function. By
        passing a data, it returns the x position on the plot.
    y : Scaler
        This argument is a scaler for y axis which behaves like a function. By
        passing a data, it returns the y position on the plot.
    width : int

    height : int

    margin_top : int
        
    margin_left : int
        
    margin_bottom : int
        
    margin_right : int
        
    color_scheme : ColorScheme | None
        
    labels : list[str] | None
        
    """
    x: Scaler
    y: Scaler
    width: int
    height: int
    margin_top: int
    margin_left: int
    margin_bottom: int
    margin_right: int
    font_size: int
    color_scheme: ColorScheme | None = None
    labels: list[str] | None = None
    labels_mapping: OrderedDict[str, str] = field(default_factory=OrderedDict)
    symbols_mapping: OrderedDict[str, str] = field(default_factory=OrderedDict)

    def get_dims(self) -> tuple[int, int]:
        return (self.width, self.height)

    def get_margin(self) -> tuple[int, int, int, int]:
        return (
            self.margin_top,
            self.margin_left,
            self.margin_bottom,
            self.margin_right,
        )
