from plotynium.marks.style import Style
from plotynium.utils.color import Color
from plotynium.utils.constant import Constant
from plotynium.interpolations import Interpolation
from plotynium.schemes import Scheme
import pytest

@pytest.fixture
def data():
    return [{"foo": x, "bar": y} for x, y in zip(range(3), range(3))]

@pytest.fixture
def default_stroke():
    return "black"

@pytest.fixture
def default_fill():
    return "none"

def test_style_default(data, default_fill, default_stroke):
    style = Style(data, default_stroke, default_fill)
    assert style._fill_opacity == 1.
    assert style._stroke_width == 1.
    assert style._stroke_opacity == 1.
    assert style._stroke_dasharray is None
    assert style._opacity == 1.
    assert isinstance(style._stroke, Constant)
    assert style._stroke(None) == default_stroke
    assert isinstance(style._fill, Constant)
    assert style._fill(None) == default_fill

def test_style_specific_values(data, default_fill, default_stroke):
    style = Style(
        data,
        default_stroke,
        default_fill,
        stroke="foo",
        fill_opacity=0.1,
        fill="bar",
        stroke_width=0.2,
        stroke_opacity=0.3,
        stroke_dasharray="1 1",
        opacity=0.4,
    )
    assert style._fill_opacity == 0.1
    assert style._stroke_width == 0.2
    assert style._stroke_opacity == 0.3
    assert style._stroke_dasharray == "1 1"
    assert style._opacity == 0.4
    assert isinstance(style._stroke, Color)
    assert isinstance(style._fill, Color)

def test_style_scheme(data, default_fill, default_stroke, monkeypatch):
    counter = [0]
    def mock_set_color_scheme(self, scheme):
        counter[0] += 1
        return
    monkeypatch.setattr(
        Color,
        "set_color_scheme",
        mock_set_color_scheme,
    )
    style = Style(data, default_stroke, default_fill, stroke="foo", fill="bar")

    assert style.scheme == Interpolation.TURBO
    style.scheme = Interpolation.SINEBOW
    assert style.scheme == Interpolation.SINEBOW
    assert counter[0] == 2
