from collections.abc import Callable

from .area import AreaY
from .axis import AxisX, AxisY
from .bar import BarX, BarY
from .dot import Dot
from .grid import GridX, GridY
from .line import Line
from .mark import Mark
from .rule import RuleY

__all__ = [
    "Dot",
    "AreaY",
    "Line",
    "BarX",
    "BarY",
    "RuleY",
    "AxisX",
    "AxisY",
    "GridX",
    "GridY",
    "Mark",
    "check_types",
]


def check_types(*types: list[type[Mark]]) -> Callable[[Mark], bool]:
    def check_mark(mark: Mark) -> bool:
        return isinstance(mark, tuple(types))

    return check_mark
