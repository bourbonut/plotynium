from dataclasses import dataclass
from math import sqrt
from typing import TypeVar

__all__ = [
    "CanvasProperties",
    "DEFAULT_LEGEND_HEIGHT",
    "DEFAULT_LEGEND_WIDTH",
    "DEFAULT_CANVAS_WIDTH",
    "DEFAULT_SQUARE_SIZE",
    "DEFAULT_SYMBOL_SIZE",
    "LegendProperties",
    "Margin",
]

TLegendProperties = TypeVar("LegendProperties", bound="LegendProperties")

DEFAULT_CANVAS_WIDTH = 640  # without legend
DEFAULT_LEGEND_WIDTH = 240
DEFAULT_LEGEND_HEIGHT = 50
DEFAULT_SQUARE_SIZE = 15
DEFAULT_SYMBOL_SIZE = 5


@dataclass
class Margin:
    """
    Dataclass to store margin values.

    Attributes
    ----------
    top : int
        Margin top value
    left : int
        Margin left value
    bottom : int
        Margin bottom value
    right : int
        Margin right value
    """

    top: int
    left: int
    bottom: int
    right: int


class Properties:
    """
    Base class for properties which has `width`, `height` and `margin` values.

    Parameters
    ----------
    width : int
        Width value
    height : int
        Height value
    margin : Margin
        Margin values
    """

    def __init__(self, width: int, height: int, margin: Margin):
        self._width = width
        self._height = height
        self._margin = margin

    def set_width(self, width: int):
        """
        Sets the width value.

        Parameters
        ----------
        width : int
            Width value to set
        """
        self._width = width

    def set_height(self, height: int):
        """
        Sets the height value.

        Parameters
        ----------
        height : int
            Height value to set
        """
        self._height = height

    def set_margin(self, margin: Margin):
        """
        Sets the margin values.

        Parameters
        ----------
        margin : Margin
            Margin values to set
        """
        self._margin = margin

    @property
    def width(self) -> int:
        """
        Returns the width value.

        Returns
        -------
        int
            Width value
        """
        return self._width

    @property
    def height(self) -> int:
        """
        Returns the height value.

        Returns
        -------
        int
            Height value
        """
        return self._height

    @property
    def margin(self) -> Margin:
        """
        Returns the margin value.

        Returns
        -------
        Margin
            Margin values
        """
        return self._margin


class CanvasProperties(Properties):
    """
    Canvas properties which has default values for `width`, `height` and
    `margin` values and has two extra attributes `translate_x` and
    `translate_y` for canvas placement.
    """

    def __init__(self):
        super().__init__(
            DEFAULT_CANVAS_WIDTH,
            int(DEFAULT_CANVAS_WIDTH / sqrt(2)),
            Margin(0, 0, 0, 0),
        )
        self._translate_x = 0
        self._translate_y = 0

    def set_translate(self, x: int = 0, y: int = 0):
        """
        Sets the translation values

        Parameters
        ----------
        x : int
            X translation value
        y : int
            Y translation value
        """
        self._translate_x = x
        self._translate_y = y

    @property
    def translate(self) -> str | None:
        """
        Returns the translation value. For instance,
        `"translate(15, 12)"` and if `x` and `y` values of the translation
        equal zero, it returns `None`.

        Returns
        -------
        str | None
            Translation value
        """
        return (
            f"translate({self._translate_x}, {self._translate_y})"
            if self._translate_x != 0 or self._translate_y != 0
            else None
        )


class LegendProperties(Properties):
    """
    Legend properties which has default values for `width`, `height` and
    `margin` values.
    """

    def __init__(self):
        super().__init__(
            DEFAULT_LEGEND_WIDTH,
            DEFAULT_LEGEND_HEIGHT,
            Margin(
                (DEFAULT_LEGEND_HEIGHT - DEFAULT_SQUARE_SIZE // 2) // 2,
                DEFAULT_SQUARE_SIZE,
                (DEFAULT_LEGEND_HEIGHT - DEFAULT_SQUARE_SIZE // 2) // 2,
                DEFAULT_SQUARE_SIZE,
            ),
        )

    @classmethod
    def new(
        self,
        width: int = 240,
        height: int = 50,
        margin_top: int = 21,
        margin_left: int = 15,
        margin_bottom: int = 21,
        margin_right: int = 15,
    ) -> TLegendProperties:
        """
        Returns legend properties given specific values.

        Parameters
        ----------
        width : int
            Width value
        height : int
            Height value
        margin_top : int
            Margin top value
        margin_left : int
            Margin left value
        margin_bottom : int
            Margin bottom value
        margin_right : int
            Margin right value

        Returns
        -------
        LegendProperties
            Legend properties filled with the given values
        """
        properties = LegendProperties()
        properties.set_width(width)
        properties.set_height(height)
        properties.set_margin(
            Margin(
                margin_top,
                margin_left,
                margin_bottom,
                margin_right,
            )
        )
        return properties
