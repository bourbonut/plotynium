from plotynium.transformers import Color, Identity, DefaultTransformer
from detroit.scale.sequential import SequentialLinear

def test_color_init():
    color = Color([{"foo": x} for x in range(3)], "foo")
    assert color.labels == [0, 1, 2]
    assert isinstance(color._color, SequentialLinear)

def test_color_try_init():
    assert isinstance(Color.try_init([], None), Identity)
    def value(d):
        return d
    transformer = Color.try_init([], value)
    assert isinstance(transformer, DefaultTransformer)
    assert transformer._transform == value
    color = Color.try_init([{"foo": x} for x in range(3)], "foo")
    assert isinstance(color, Color)

def test_color_call():
    color = Color([{"foo": x} for x in range(3)], "foo")
    assert isinstance(color({"foo": 0}), str)
