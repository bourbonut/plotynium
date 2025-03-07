from plotynium.utils.color import Color
from detroit.scale.sequential import SequentialLinear

def test_color_init():
    color = Color([{"foo": x} for x in range(3)], "foo")
    assert color.labels == [0, 1, 2]
    assert isinstance(color._color, SequentialLinear)

def test_color_try_init():
    assert Color.try_init([], None) is None
    value = lambda d: d
    assert Color.try_init([], value) == value
    color = Color.try_init([{"foo": x} for x in range(3)], "foo")
    assert isinstance(color, Color)

def test_color_call():
    color = Color([{"foo": x} for x in range(3)], "foo")
    assert isinstance(color({"foo": 0}), str)
