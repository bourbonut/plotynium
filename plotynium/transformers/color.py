from collections.abc import Callable

import detroit as d3

from ..interpolations import Interpolation
from ..schemes import Scheme
from ..types import ColorScheme, Data, Index, T
from .default import DefaultTransformer
from .getter import getter
from .identity import Identity
from .picker import LegendPicker
from .transformer import Transformer


def default_colorscheme(nb_labels: int) -> Interpolation | Scheme:
    if nb_labels > 10:
        return Interpolation.RAINBOW
    else:
        return Scheme.OBSERVABLE_10


class QualitativeScaler:
    """
    Combination of a band scaler and a sequential scaler.
    The band scaler helps for making a number given a string.
    The sequential scaler takes a number and returns a color.

    Parameters
    ----------
    labels : list[str]
        List of labels
    """

    def __init__(self, labels: list[str]):
        nb_labels = len(labels)
        self._band = d3.scale_band(labels, [0, nb_labels])
        self._sequential = d3.scale_sequential(
            [0, nb_labels - 1], default_colorscheme(nb_labels)
        )

    def __call__(self, d):
        return self._sequential(self._band(d))

    def set_interpolator(self, interpolator):
        self._sequential.set_interpolator(interpolator)


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
            self._color = d3.scale_sequential(
                [min(data), max(data)], default_colorscheme(len(self.labels))
            )
        self._picker = LegendPicker()

    def __call__(self, d: T) -> str:
        """
        Transforms a data into a color.

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
        return self._picker(value, color)

    def set_color_scheme(self, scheme: ColorScheme):
        """
        Sets the color scheme.

        Parameters
        ----------
        scheme : Interpolation | Scheme
            Parameter for color scheme
        """
        self._color.set_interpolator(scheme)

    def set_labels(self, labels: dict[int, str]):
        """
        Sets labels to the legend picker

        Parameters
        ----------
        labels : dict[int, str]
            Dictionary of labels where keys is the index of the label and
            values are each label
        """
        self._picker = LegendPicker(labels)

    def get_mapping(self) -> list[tuple[str, str]]:
        """
        Returns the mapping of the picker.

        Returns
        -------
        list[tuple[str, str]]
            List of pairs (labels, colors).
        """
        return self._picker.get_mapping()

    @staticmethod
    def try_init(
        data: list[T],
        value: str | Index | Callable[[T], str] | None = None,
        default: Transformer[T, str] | None = None,
    ) -> Transformer[T, str] | None:
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
        Transformer[T, str] | None
           `Color` if `value` is an index or a key value else it could be directly
           `value` when it is callable. If all arguments are `None` (except `data`),
           the function returns `None`.
        """
        if callable(value):
            return DefaultTransformer(data, value)
        elif len(data) > 0 and (
            (isinstance(value, str) and value in data[0])
            or (isinstance(value, int) and value < len(data[0]))
        ):
            return Color(data, value)
        else:
            return Identity() if default is None else default
