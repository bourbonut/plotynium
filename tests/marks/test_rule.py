from plotynium.marks.rule import RuleY
from plotynium.utils.constant import Constant
from plotynium.scaler import Scaler
import detroit as d3
import pytest

from datetime import datetime

def test_rule_y_default():
    rule_y = RuleY([0, 1])
    assert rule_y.x_label is None
    assert rule_y.y_label is None
    assert rule_y.x_domain is None
    assert rule_y.y_domain == [0, 1]
    assert rule_y.x_scaler_type is None
    assert rule_y.y_scaler_type == Scaler.CONTINUOUS

    assert rule_y._fill_opacity == 1.
    assert rule_y._stroke_width == 1.5
    assert rule_y._stroke_opacity == 1.
    assert rule_y._stroke_dasharray is None
    assert rule_y._opacity == 1.
    assert isinstance(rule_y._stroke, Constant)
    assert rule_y._stroke(None) == "black"
    assert isinstance(rule_y._fill, Constant)
    assert rule_y._fill(None) == "none"

@pytest.mark.parametrize("values", [[0], [datetime.now()]])
def test_rule_y_call(values):
    rule_y = RuleY(values)
    svg = d3.create("svg")
    rule_y(svg, d3.scale_linear(), d3.scale_linear())
    g = svg.select("g.rule")
    assert len(g.nodes()) == 1
    path = g.select("path")
    assert len(path.nodes()) == 1
