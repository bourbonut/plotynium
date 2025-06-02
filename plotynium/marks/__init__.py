from collections.abc import Callable

from .area import AreaY
from .axis import AxisX, AxisY
from .bar import BarX, BarY
from .dot import Dot
from .grid import GridX, GridY
from .line import Line
from .mark import Mark
from .rule import RuleX, RuleY

__all__ = [
    "Dot",
    "AreaY",
    "Line",
    "BarX",
    "BarY",
    "RuleX",
    "RuleY",
    "AxisX",
    "AxisY",
    "GridX",
    "GridY",
    "Mark",
    "check_types",
]


def check_types(*types: list[type[Mark]]) -> Callable[[Mark], bool]:
    """
    Builds a function for checking different mark types


    Parameters
    ----------
    types : list[type[Mark]]
        Mark types to be checked

    Returns
    -------
    Callable[[Mark], bool]
        Function takes a `Mark` object as input and returns if the object is
        one of the types given by the `check_types` function itself.
    """

    def check_mark(mark: Mark) -> bool:
        return isinstance(mark, tuple(types))

    return check_mark
