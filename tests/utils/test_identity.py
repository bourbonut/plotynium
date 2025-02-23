from plotynium.utils.identity import Identity
import pytest

@pytest.mark.parametrize(
    "value",
    [None, 10, -11, "foo", {"some": "value"}]
)
def test_identity(value):
    identity = Identity()
    assert identity(value) == value
