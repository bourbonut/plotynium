from plotynium.marks.dot import Dot, center
from plotynium.utils.constant import Constant
from plotynium.utils.identity import Identity
from plotynium.utils.symbol import Symbol
from plotynium.scaler import Scaler
import detroit as d3
from detroit.scale.band import ScaleBand
from detroit.scale.linear import ScaleLinear
import pytest

def test_center():
    scale = d3.scale_band()
    assert not isinstance(center(scale), ScaleBand)
    scale = d3.scale_linear()
    assert isinstance(center(scale), ScaleLinear)

def test_dot_default():
    dot = Dot([[x, y] for x, y in zip(range(11), range(11))])
    assert dot.x_label is None
    assert dot.y_label is None
    assert dot.x_domain == [0, 10]
    assert dot.y_domain == [0, 10]
    assert dot.x_scaler_type == Scaler.CONTINUOUS
    assert dot.y_scaler_type == Scaler.CONTINUOUS

    assert isinstance(dot._r, Constant)
    assert dot._r(None) == 3
    assert dot._symbol is None
    assert dot.legend_labels == []

    assert dot._fill_opacity == 1.
    assert dot._stroke_width == 1.5
    assert dot._stroke_opacity == 1.
    assert dot._stroke_dasharray is None
    assert dot._opacity == 1.
    assert isinstance(dot._stroke, Constant)
    assert dot._stroke(None) == "black"
    assert isinstance(dot._fill, Constant)
    assert dot._fill(None) == "none"

def test_dot_symbol():
    data = [
        {"x": x, "y": y, "label": label}
        for x, y, label in zip(range(11), range(11), "aaaabbbcccc")
    ]
    dot = Dot(data, x="x", y="y", symbol="label")
    assert dot.x_label == "x"
    assert dot.y_label == "y"
    assert dot.x_domain == [0, 10]
    assert dot.y_domain == [0, 10]
    assert dot.x_scaler_type == Scaler.CONTINUOUS
    assert dot.y_scaler_type == Scaler.CONTINUOUS

    assert isinstance(dot._r, Constant)
    assert dot._r(None) == 3
    assert isinstance(dot._symbol, Symbol)
    assert dot.legend_labels == ["a", "b", "c"]

def test_dot_call_circle():
    dot = Dot([[x, y] for x, y in zip(range(11), range(11))])
    svg = d3.create("svg")
    dot(svg, d3.scale_linear(), d3.scale_linear())
    g = svg.select("g.dots").select_all("circle")
    assert len(g.nodes()) == 11

def test_dot_call_symbol():
    data = [
        {"x": x, "y": y, "label": label}
        for x, y, label in zip(range(11), range(11), "aaaabbbcccc")
    ]
    dot = Dot(data, x="x", y="y", symbol="label")
    svg = d3.create("svg")
    dot(svg, d3.scale_linear(), d3.scale_linear())
    g = svg.select("g.dots").select_all("path")
    assert len(g.nodes()) == 11
