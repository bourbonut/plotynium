from plotynium.marks.bar import BarY
from plotynium.utils.constant import Constant
from plotynium.scaler import Scaler
import pytest
import detroit as d3
import random
from copy import copy

from datetime import datetime

def test_bar_y_default():
    bar_y = BarY([[x, y] for x, y in zip("aaabbbcccdd", range(11))])

    assert bar_y.x_label is None
    assert bar_y.y_label is None
    assert bar_y.x_domain == ["a", "b", "c", "d"]
    assert bar_y.y_domain == [0, 10]
    assert bar_y.x_scaler_type == Scaler.BAND
    assert bar_y.y_scaler_type == Scaler.CONTINUOUS
    assert bar_y.legend_labels == []

    assert bar_y._fill_opacity == 1.
    assert bar_y._stroke_width == 1.
    assert bar_y._stroke_opacity == 1.
    assert bar_y._stroke_dasharray is None
    assert bar_y._opacity == 1.
    assert isinstance(bar_y._stroke, Constant)
    assert bar_y._stroke(None) == "none"
    assert isinstance(bar_y._fill, Constant)
    assert bar_y._fill(None) == "black"

def test_bar_y_sort_by():
    data = [
        {"letter": letter, "freq": freq / 10}
        for letter, freq in zip("aaabbbcccdd", range(11))
    ]
    copied = copy(data)
    random.shuffle(copied)
    bar_y = BarY(copied, x="letter", y="freq", sort={"by": "freq", "descending": True})
    assert bar_y._data == list(reversed(data))

def test_bar_y_call():
    bar_y = BarY([[x, y] for x, y in zip("aaabbbcccdd", range(11))])
    svg = d3.create("svg")
    bar_y(svg, d3.scale_band(), d3.scale_linear())
    g = svg.select("g.bars")
    assert len(g.nodes()) == 1
    path = svg.select_all("rect")
    assert len(path.nodes()) == 11
