from ..options import ColorOptions
from ..schemes import Scheme
from ..interpolations import Interpolation
from ..types import Index, T, Data
from ..getter import getter
from .transformer import Transformer
from .picker import LegendPicker
from typing import Any
from collections.abc import Callable
import detroit as d3

class QualitativeScaler:
    def __init__(self, labels):
        self._band = d3.scale_band(labels, [0, len(labels)])
        self._ordinal = d3.scale_sequential([0, len(labels) - 1], ColorOptions().scheme)

    def __call__(self, d):
        return self._ordinal(self._band(d))

    def set_interpolator(self, interpolator):
        self._ordinal.set_interpolator(interpolator)

class Color(Transformer[T, str]):
    """
    This class makes a sequential scaler which generates color values based on data.

    Parameters
    ----------
    data : list[T]
        List of data
    value : str | Index | Callable[[T], Data]
        Index or key value for accessing data
    """
    def __init__(self, data: list[T], value: str | Index | Callable[[T], Data]):
        self._value = getter(value)
        data = list(map(self._value, data))
        self.labels = sorted(set(data))
        sample = self.labels[0]
        if isinstance(sample, str):
            self._color = QualitativeScaler(self.labels)
        else:
            self._color = d3.scale_sequential([min(data), max(data)], ColorOptions().scheme)
        self._picker = LegendPicker()

    def __call__(self, d: T) -> str:
        """
        Transforms a data into a color

        Parameters
        ----------
        d : T
            Data input

        Returns
        -------
        str
            Color string formatted as RGB or HEX depending on the color scheme
        """
        value = self._value(d)
        color = self._color(value)
        return self._picker(color)

    def set_color_scheme(self, scheme: Interpolation | Scheme):
        """
        Sets the color scheme

        Parameters
        ----------
        scheme : Interpolation | Scheme
            Parameter for color scheme
        """
        self._color.set_interpolator(scheme)

    @staticmethod
    def try_init(
        data: list[T],
        value: str | Index | Callable[[T], str] | None = None,
        default: Transformer[T, str] | None = None,
    ) -> Callable[[T], str] | None:
        """
        If `values` is a callable, it returns it.
        Else it creates a `Color` depending on `value` type.

        Parameters
        ----------
        data : list[T]
            Data input used for `Color` if `value` is not callable
        value : str | Index | Callable[[T], str] | None
            Depending of the type, it is used for `Color` or directly returned by the
            function
        default : Transformer[T, str] | None
            Default value used as second argument of `Color` if `value` is `None`

        Returns
        -------
        Callable[[T], str] | None
           `Color` if `value` is an index or a key value else it could be directly
           `value` when it is callable. If all arguments are `None` (except `data`),
           the function returns `None`.
        """
        if callable(value):
            return value
        elif len(data) > 0 and (
            (
                isinstance(value, str) and value in data[0]
            ) or (
                isinstance(value, int) and value < len(data[0])
            )
        ):
            return Color(data, value)
        else:
            return default
