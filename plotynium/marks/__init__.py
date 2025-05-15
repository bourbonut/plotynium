from .dot import Dot
from .area import AreaY
from .line import Line
from .bar import BarY
from .rule import RuleY
from .axis import AxisX, AxisY
from .grid import GridX, GridY
from .mark import Mark

from collections.abc import Callable

__all__ = [
    "Dot",
    "AreaY",
    "Line",
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
