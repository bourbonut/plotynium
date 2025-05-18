from collections.abc import Callable
from typing import Generic

from ..transformers import Color, Constant
from ..types import ColorScheme, T


class Style(Generic[T]):
    """
    Primary class for managing all style values.

    Parameters
    ----------
    data: list[T]
        List of data used for `fill` and `stroke` attributes
    default_stroke: str
        Default constant value for `stroke` attribute.
    default_fill: str
        Default constant value for `fill` attribute.
    fill: Callable[[T], str] | str | None
        Function which takes a data and returns a color applied for `fill` attribute.
    fill_opacity: float
        Fill opacity value included in [0, 1].
    stroke: Callable[[T], str] | str | None
        Function which takes a data and returns a color applied for `stroke` attribute.
    stroke_width : float
        Stroke width value.
    stroke_opacity : float
        Stroke opacity value included in [0, 1].
    stroke_dasharray : str | None
        Stroke dasharray value.
    opacity : float
        General opacity value included in [0, 1].
    """

    def __init__(
        self,
        data: list[T],
        default_stroke: str,
        default_fill: str,
        fill: Callable[[T], str] | str | None = None,
        fill_opacity: float = 1.0,
        stroke: Callable[[T], str] | str | None = None,
        stroke_width: float = 1.0,
        stroke_opacity: float = 1.0,
        stroke_dasharray: str | None = None,
        opacity: float = 1.0,
    ):
        self._fill = Color.try_init(data, fill, Constant(fill or default_fill))
        self._fill_opacity = fill_opacity

        self._stroke = Color.try_init(data, stroke, Constant(stroke or default_stroke))
        self._stroke_width = stroke_width
        self._stroke_dasharray = stroke_dasharray
        self._stroke_opacity = stroke_opacity
        self._opacity = opacity

    def set_colorscheme(self, scheme: ColorScheme | None = None):
        """
        Sets the color scheme

        Parameters
        ----------
        scheme : ColorScheme | None
            Color scheme to be set
        """
        if scheme is not None:
            self._fill.set_color_scheme(scheme)
            self._stroke.set_color_scheme(scheme)

    def set_labels(self, labels: dict[int, str]):
        """
        Sets labels for *stroke* and *fill* attributes.

        Parameters
        ----------
        labels : dict[int, str]
            Dictionary of labels where keys is the index of the label and
            values are each label
        """
        self._stroke.set_labels(labels)
        self._fill.set_labels(labels)
