from plotynium.utils.symbol import Symbol
from detroit.scale.ordinal import ScaleOrdinal

def test_symbol_init():
    symbol = Symbol([{"foo": x} for x in "cba"], "foo")
    assert symbol.labels == ["a", "b", "c"]
    assert isinstance(symbol._symbol_type, ScaleOrdinal)

def test_symbol_try_init():
    assert Symbol.try_init([], None) is None
    value = lambda d: d
    assert Symbol.try_init([], value) == value
    symbol = Symbol.try_init([{"foo": x} for x in "cba"], "foo")
    assert isinstance(symbol, Symbol)

def test_symbol_call():
    symbol = Symbol([{"foo": x} for x in "cba"], "foo")
    assert isinstance(symbol({"foo": "a"}), str)
