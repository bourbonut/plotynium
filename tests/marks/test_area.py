from datetime import datetime

import detroit as d3
import pytest

from plotynium.marks.area import AreaY
from plotynium.scaler import Scaler
from plotynium.transformers import Constant
from tests.default_context import default_context


def test_area_y_default():
    area_y = AreaY([[x, y] for x, y in zip(range(11), range(11))])

    assert area_y.x_label is None
    assert area_y.y_label is None
    assert area_y.x_domain == [0, 10]
    assert area_y.y_domain == [0, 10]
    assert area_y.x_scaler_type == Scaler.CONTINUOUS
    assert area_y.y_scaler_type == Scaler.CONTINUOUS

    assert area_y._fill_opacity == 1.0
    assert area_y._stroke_width == 1.0
    assert area_y._stroke_opacity == 1.0
    assert area_y._stroke_dasharray is None
    assert area_y._opacity == 1.0
    assert isinstance(area_y._stroke, Constant)
    assert area_y._stroke(None) == "none"
    assert isinstance(area_y._fill, Constant)
    assert area_y._fill(None) == "black"


def test_area_y_error():
    with pytest.raises(ValueError):
        AreaY([[x, y] for x, y in zip(range(11), range(11))], y1=lambda d: d)


@pytest.mark.parametrize(
    "area_y",
    [
        AreaY([[x, y] for x, y in zip(range(11), range(11))]),
        AreaY([[datetime.now(), y] for x, y in zip(range(11), range(11))]),
    ],
)
def test_area_y_call(area_y):
    svg = d3.create("svg")
    area_y.apply(svg, default_context(d3.scale_linear(), d3.scale_linear()))
    g = svg.select("g.area")
    assert len(g.nodes()) == 1
    path = svg.select("path")
    assert len(path.nodes()) == 1
