from math import sqrt
from .marks import AxisX, AxisY, Mark, check_types
from .legends import Legend
from .properties import DEFAULT_LEGEND_WIDTH, DEFAULT_LEGEND_HEIGHT, DEFAULT_CANVAS_WIDTH

def auto_width(legend_width: bool, only_legend: bool, has_legend: bool) -> int:
    if only_legend and has_legend:
        return legend_width
    else:
        return DEFAULT_CANVAS_WIDTH

def auto_height(
    width: int,
    legend_height: int,
    only_axis: bool,
    axis_is_x: bool,
    has_legend: bool,
    only_legend: bool,
) -> int:
    if (only_legend and has_legend) or (only_axis and axis_is_x):
        return legend_height
    elif has_legend:
        return legend_height + int(width / sqrt(2))
    return int(width / sqrt(2))

def dimensions(
    marks: list[Mark],
    user_legend_option: bool,
    width: int | None = None,
    height: int | None = None,
) -> tuple[int, int]:
    axis_marks = list(filter(check_types(AxisX, AxisY), marks))
    only_axis = len(axis_marks) == 1
    axis_is_x = isinstance(axis_marks[0], AxisX) if only_axis else False
    legend_marks = list(filter(check_types(Legend), marks))
    has_legend = len(legend_marks) >= 1 or user_legend_option
    only_legend = len(legend_marks) == 1
    legend_width = DEFAULT_LEGEND_WIDTH
    legend_height = DEFAULT_LEGEND_HEIGHT
    if len(legend_marks) > 1:
        raise ValueError("There can be only one legend.")
    elif len(legend_marks) == 1:
        legend_width = legend_marks[0]._width
        legend_height = legend_marks[0]._height

    # Set dimensions
    width = width or auto_width(legend_width, only_legend, has_legend)
    height = height or auto_height(
        width, legend_height, only_axis, axis_is_x, has_legend, only_legend
    )
    return width, height
