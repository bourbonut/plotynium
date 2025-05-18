import detroit as d3

from plotynium.marks.grid import GridX, GridY
from plotynium.properties import CanvasProperties, Margin
from plotynium.scaler import Scaler
from tests.default_context import default_context


def test_grid_x_default():
    grid_x = GridX()

    assert grid_x._data == [x / 10 for x in range(11)]
    assert grid_x.x_label is None
    assert grid_x.y_label is None
    assert grid_x.x_domain == [0.0, 1.0]
    assert grid_x.y_domain is None
    assert grid_x.x_scaler_type == Scaler.CONTINUOUS
    assert grid_x.y_scaler_type is None

    assert grid_x._stroke == "currentColor"
    assert grid_x._stroke_width == 1.0
    assert grid_x._stroke_opacity == 0.1
    assert grid_x._stroke_dasharray is None


def test_grid_x_call():
    grid_x = GridX()
    svg = d3.create("svg")
    margin = Margin(20, 0, 10, 0)
    canvas_properties = CanvasProperties()
    canvas_properties.set_height(400)
    canvas_properties.set_margin(margin)
    grid_x.apply(
        svg, default_context(d3.scale_linear(), d3.scale_linear(), canvas_properties)
    )
    g = svg.select("g")

    assert len(g.nodes()) == 1
    lines = g.select_all("line")
    assert len(lines.nodes()) == 11


def test_grid_y_default():
    grid_y = GridY()

    assert grid_y._data == [x / 10 for x in range(11)]
    assert grid_y.x_label is None
    assert grid_y.y_label is None
    assert grid_y.x_domain is None
    assert grid_y.y_domain == [0.0, 1.0]
    assert grid_y.x_scaler_type is None
    assert grid_y.y_scaler_type == Scaler.CONTINUOUS

    assert grid_y._stroke == "currentColor"
    assert grid_y._stroke_width == 1.0
    assert grid_y._stroke_opacity == 0.1
    assert grid_y._stroke_dasharray is None


def test_grid_y_call():
    grid_y = GridY()
    svg = d3.create("svg")
    margin = Margin(0, 20, 0, 10)
    canvas_properties = CanvasProperties()
    canvas_properties.set_width(400)
    canvas_properties.set_margin(margin)
    grid_y.apply(
        svg, default_context(d3.scale_linear(), d3.scale_linear(), canvas_properties)
    )
    g = svg.select("g")

    assert len(g.nodes()) == 1
    lines = g.select_all("line")
    assert len(lines.nodes()) == 11
