from math import sqrt

import pytest
from plotynium.dimensions import auto_height, auto_width, dimensions
from plotynium.legends import Legend
from plotynium.marks.axis import AxisX, AxisY
from plotynium.properties import CanvasProperties, LegendProperties, Margin


@pytest.mark.parametrize(
    "only_legend, has_legend, width, expected_width",
    [
        [False, False, None, 640],
        [True, False, None, 640],
        [False, True, None, 640],
        [True, True, None, 240],
        [False, False, 1000, 1000],
        [True, False, 1000, 1000],
        [False, True, 1000, 1000],
        [True, True, 1000, 240],
    ],
)
def test_auto_width(
    only_legend,
    has_legend,
    width,
    expected_width,
):
    canvas_properties = CanvasProperties()
    assert (
        auto_width(
            canvas_properties, LegendProperties(), only_legend, has_legend, width
        )
        == expected_width
    )
    if width is not None and not (only_legend and has_legend):
        assert canvas_properties.width == width


@pytest.mark.parametrize(
    (
        "only_axis, "
        "axis_is_x, "
        "has_legend, "
        "only_legend, "
        "width, "
        "height, "
        "expected_height, "
        "expected_canvas_height"
    ),
    [
        [False, False, False, False, None, None, int(640 / sqrt(2)), None],
        [True, False, False, False, None, None, int(640 / sqrt(2)), None],
        [True, True, False, False, None, None, 50, None],
        [False, False, True, True, None, None, 50, None],
        [
            False,
            False,
            True,
            False,
            None,
            None,
            int(640 / sqrt(2)) + 50,
            int(640 / sqrt(2)),
        ],
        [False, False, True, False, None, 200, 200 + 50, 200],
        [False, False, False, False, 200, 200, 200, None],
    ],
)
def test_auto_height(
    only_axis,
    axis_is_x,
    has_legend,
    only_legend,
    width,
    height,
    expected_height,
    expected_canvas_height,
):
    canvas_properties = CanvasProperties()
    if width is not None:
        canvas_properties.set_width(width)
    legend_properties = LegendProperties()
    assert (
        auto_height(
            canvas_properties,
            legend_properties,
            only_axis,
            axis_is_x,
            has_legend,
            only_legend,
            height,
        )
        == expected_height
    )
    assert canvas_properties.height == (expected_canvas_height or expected_height)


@pytest.mark.parametrize(
    (
        "marks, "
        "user_legend_option, "
        "width, "
        "height, "
        "margin, "
        "expected_width, "
        "expected_height, "
        "expected_canvas_width, "
        "expected_canvas_height, "
        "expected_canvas_margin, "
        "expected_legend_width, "
        "expected_legend_height"
    ),
    [
        [
            [],
            False,
            None,
            None,
            None,
            640,
            int(640 / sqrt(2)),
            None,
            None,
            Margin(0, 0, 0, 0),
            240,
            50,
        ],
        [
            [],
            True,
            None,
            None,
            None,
            640,
            int(640 / sqrt(2)) + 50,
            None,
            int(640 / sqrt(2)),
            Margin(0, 0, 0, 0),
            240,
            50,
        ],
        [
            [],
            False,
            500,
            None,
            None,
            500,
            int(500 / sqrt(2)),
            None,
            None,
            Margin(0, 0, 0, 0),
            240,
            50,
        ],
        [[], False, None, 200, None, 640, 200, None, None, Margin(0, 0, 0, 0), 240, 50],
        [
            [],
            False,
            None,
            None,
            Margin(1, 2, 3, 4),
            640,
            int(640 / sqrt(2)),
            None,
            None,
            Margin(1, 2, 3, 4),
            240,
            50,
        ],
        [
            [Legend(width=100)],
            False,
            None,
            None,
            None,
            100,
            50,
            640,
            50,
            Margin(0, 0, 0, 0),
            100,
            50,
        ],
        [
            [AxisX()],
            False,
            None,
            None,
            None,
            640,
            50,
            640,
            50,
            Margin(0, 0, 0, 0),
            240,
            50,
        ],
        [
            [AxisY()],
            False,
            None,
            None,
            None,
            640,
            int(640 / sqrt(2)),
            None,
            None,
            Margin(0, 0, 0, 0),
            240,
            50,
        ],
    ],
)
def test_dimensions(
    marks,
    user_legend_option,
    width,
    height,
    margin,
    expected_width,
    expected_height,
    expected_canvas_width,
    expected_canvas_height,
    expected_canvas_margin,
    expected_legend_width,
    expected_legend_height,
):
    (width, height, canvas_properties, legend_properties) = dimensions(
        marks, user_legend_option, width, height, margin
    )
    assert width == expected_width
    assert height == expected_height
    assert canvas_properties.width == (expected_canvas_width or expected_width)
    assert canvas_properties.height == (expected_canvas_height or expected_height)
    assert canvas_properties.margin == expected_canvas_margin
    assert legend_properties.width == expected_legend_width
    assert legend_properties.height == expected_legend_height
