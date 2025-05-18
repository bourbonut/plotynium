import pytest

from plotynium.transformers import Constant


@pytest.mark.parametrize("value", [None, 10, -11, "foo"])
def test_constant(value):
    constant = Constant(value)
    assert constant({"unknown": "value"}) == value


def test_constant_error():
    constant = Constant({"some": "value"})
    with pytest.raises(TypeError):
        constant({"unknown": "value"})
