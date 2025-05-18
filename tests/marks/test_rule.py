from datetime import datetime

import detroit as d3
import pytest

from plotynium.marks.rule import RuleY
from plotynium.scaler import Scaler
from plotynium.transformers import Constant
from tests.default_context import default_context


def test_rule_y_default():
    rule_y = RuleY([0, 1])
    assert rule_y.x_label is None
    assert rule_y.y_label is None
    assert rule_y.x_domain is None
    assert rule_y.y_domain == [0, 1]
    assert rule_y.x_scaler_type is None
    assert rule_y.y_scaler_type == Scaler.CONTINUOUS

    assert rule_y._fill_opacity == 1.0
    assert rule_y._stroke_width == 1.5
    assert rule_y._stroke_opacity == 1.0
    assert rule_y._stroke_dasharray is None
    assert rule_y._opacity == 1.0
    assert isinstance(rule_y._stroke, Constant)
    assert rule_y._stroke(None) == "black"
    assert isinstance(rule_y._fill, Constant)
    assert rule_y._fill(None) == "none"


@pytest.mark.parametrize("values", [[0], [datetime.now()]])
def test_rule_y_call(values):
    rule_y = RuleY(values)
    svg = d3.create("svg")
    rule_y.apply(svg, default_context(d3.scale_linear(), d3.scale_linear()))
    g = svg.select("g.rule")
    assert len(g.nodes()) == 1
    path = g.select("path")
    assert len(path.nodes()) == 1
