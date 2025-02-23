from plotynium.utils.constant import Constant
import pytest

@pytest.mark.parametrize(
    "value",
    [None, 10, -11, "foo", {"some": "value"}]
)
def test_identity(value):
    identity = Constant(value)
    assert identity({"unknown": "value"}) == value
