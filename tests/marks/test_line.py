from datetime import datetime

import detroit as d3
import pytest

from plotynium.marks.line import Line
from plotynium.scaler import Scaler
from plotynium.transformers import Constant
from tests.default_context import default_context


def test_line_default():
    line = Line([[x, y] for x, y in zip(range(11), range(11))])

    assert line.x_label is None
    assert line.y_label is None
    assert line.x_domain == [0, 10]
    assert line.y_domain == [0, 10]
    assert line.x_scaler_type == Scaler.CONTINUOUS
    assert line.y_scaler_type == Scaler.CONTINUOUS

    assert line._fill_opacity == 1.0
    assert line._stroke_width == 1.0
    assert line._stroke_opacity == 1.0
    assert line._stroke_dasharray is None
    assert line._opacity == 1.0
    assert isinstance(line._stroke, Constant)
    assert line._stroke(None) == "black"
    assert isinstance(line._fill, Constant)
    assert line._fill(None) == "none"


@pytest.mark.parametrize(
    "line",
    [
        Line([[x, y] for x, y in zip(range(11), range(11))]),
        Line([[datetime.now(), y] for x, y in zip(range(11), range(11))]),
    ],
)
def test_line_call(line):
    svg = d3.create("svg")
    line.apply(svg, default_context(d3.scale_linear(), d3.scale_linear()))
    g = svg.select("g.line")
    assert len(g.nodes()) == 1
    path = svg.select("path")
    assert len(path.nodes()) == 1
