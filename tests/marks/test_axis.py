from plotynium.marks.axis import AxisX, AxisY
from plotynium.utils.constant import Constant
from plotynium.utils.identity import Identity
from plotynium.scaler import Scaler
import detroit as d3
import pytest

from datetime import datetime

def test_axis_x_default():
    axis_x = AxisX()
    assert axis_x._data == [x / 10 for x in range(11)]
    assert axis_x.x_label is None
    assert axis_x.y_label is None
    assert axis_x.x_domain == [0., 1.]
    assert axis_x.y_domain is None
    assert axis_x.x_scaler_type == Scaler.CONTINUOUS
    assert axis_x.y_scaler_type is None

    assert axis_x._anchor == "bottom"
    assert axis_x._tick_rotate == 0.
    assert axis_x._tick_size == 6
    assert isinstance(axis_x._tick_format, Identity)

    assert axis_x._stroke == "currentColor"
    assert axis_x._fill == "inherit"
    assert axis_x._stroke_width == 1.
    assert axis_x._stroke_opacity == 1.


@pytest.mark.parametrize(
    "axis_x, ngroups",
    [
        [AxisX(list(range(11))), 2],
        [AxisX(list(range(11)), label="x label"), 3],
    ]
)
def test_axis_x_call(axis_x, ngroups):
    svg = d3.create("svg")
    axis_x(
        svg,
        d3.scale_linear(),
        d3.scale_linear(),
        height=400,
        margin_top=10,
        margin_bottom=20,
    )
    g = svg.select_all("g")
    assert len(g.nodes()) == ngroups

def test_axis_y_default():
    axis_y = AxisY()
    assert axis_y._data == [x / 10 for x in range(11)]
    assert axis_y.x_label is None
    assert axis_y.y_label is None
    assert axis_y.x_domain is None
    assert axis_y.y_domain == [0., 1.]
    assert axis_y.x_scaler_type is None
    assert axis_y.y_scaler_type == Scaler.CONTINUOUS

    assert axis_y._anchor == "left"
    assert axis_y._tick_rotate == 0.
    assert axis_y._tick_size == 6
    assert isinstance(axis_y._tick_format, Identity)

    assert axis_y._stroke == "currentColor"
    assert axis_y._fill == "inherit"
    assert axis_y._stroke_width == 1.
    assert axis_y._stroke_opacity == 1.


@pytest.mark.parametrize(
    "axis_y, ngroups",
    [
        [AxisY(list(range(11))), 2],
        [AxisY(list(range(11)), label="y label"), 3],
    ]
)
def test_axis_y_call(axis_y, ngroups):
    svg = d3.create("svg")
    axis_y(
        svg,
        d3.scale_linear(),
        d3.scale_linear(),
        width=400,
        margin_left=10,
        margin_right=20,
    )
    g = svg.select_all("g")
    assert len(g.nodes()) == ngroups
