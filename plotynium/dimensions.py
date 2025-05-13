from math import sqrt
from .marks import AxisX, AxisY, Mark, check_types
from .legends import Legend
from .properties import CanvasProperties, LegendProperties, Margin

def auto_width(
    canvas_properties: CanvasProperties,
    legend_properties: LegendProperties,
    only_legend: bool,
    has_legend: bool,
    width: int | None = None,
) -> int:
    if only_legend and has_legend: # only legend
        return legend_properties.width
    elif width is None: # no user width
        return max(canvas_properties.width, legend_properties.width)
    else: # user width
        canvas_properties.set_width(width)
        return max(width, legend_properties.width)

def auto_height(
    canvas_properties: CanvasProperties,
    legend_properties: LegendProperties,
    only_axis: bool,
    axis_is_x: bool,
    has_legend: bool,
    only_legend: bool,
    height: int | None = None,
) -> int:
    legend_height = legend_properties.height
    if (only_legend and has_legend) or (only_axis and axis_is_x): # only legend
        return legend_height
    elif has_legend and height is None: # legend and no user height
        height = int(canvas_properties.width / sqrt(2))
        canvas_properties.set_height(height)
        canvas_properties.set_translate(0, legend_height)
        return legend_height + height
    elif has_legend: # legend and user height
        canvas_properties.set_height(height)
        canvas_properties.set_translate(0, legend_height)
        return legend_height + height
    else: # no legend and user height
        height = int(canvas_properties.width / sqrt(2))
        canvas_properties.set_height(height)
        return height

def dimensions(
    marks: list[Mark],
    user_legend_option: bool,
    width: int | None = None,
    height: int | None = None,
    margin: Margin | None = None,
) -> tuple[int, int, CanvasProperties, LegendProperties]:
    # Analyze axis marks
    axis_marks = list(filter(check_types(AxisX, AxisY), marks))
    only_axis = len(axis_marks) == 1
    axis_is_x = isinstance(axis_marks[0], AxisX) if only_axis else False

    # Analyze legend marks
    legend_marks = list(filter(check_types(Legend), marks))
    has_legend = len(legend_marks) >= 1 or user_legend_option
    only_legend = len(legend_marks) == 1

    # Sets legend properties
    legend_properties = LegendProperties()
    if len(legend_marks) > 1:
        raise ValueError("There can be only one legend.")
    elif len(legend_marks) == 1:
        legend_properties = legend_marks[0].properties

    # Creates canvas properties
    canvas_properties = CanvasProperties()
    if margin is not None:
        canvas_properties.set_margin(margin)

    # Set dimensions
    width = auto_width(
        canvas_properties,
        legend_properties,
        only_legend,
        has_legend,
        width=width,
    )
    height = auto_height(
        canvas_properties,
        legend_properties,
        only_axis,
        axis_is_x,
        has_legend,
        only_legend,
        height=height,
    )
    return width, height, canvas_properties, legend_properties
