from plotynium.transformers import Symbol, Identity, DefaultTransformer
from detroit.scale.ordinal import ScaleOrdinal

def test_symbol_init():
    symbol = Symbol([{"foo": x} for x in "cba"], "foo")
    assert symbol._labels == ["a", "b", "c"]
    assert isinstance(symbol._symbol_type, ScaleOrdinal)

def test_symbol_try_init():
    assert isinstance(Symbol.try_init([], None), Identity)
    def value(d):
        return d
    transform = Symbol.try_init([], value)
    assert isinstance(transform, DefaultTransformer)
    assert transform._transform == value
    symbol = Symbol.try_init([{"foo": x} for x in "cba"], "foo")
    assert isinstance(symbol, Symbol)

def test_symbol_call():
    symbol = Symbol([{"foo": x} for x in "cba"], "foo")
    assert isinstance(symbol({"foo": "a"}), str)
