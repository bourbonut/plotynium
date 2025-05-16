from plotynium.transformers import Identity
import pytest

@pytest.mark.parametrize(
    "value",
    [None, 10, -11, "foo"]
)
def test_identity(value):
    identity = Identity()
    assert identity(value) == value

def test_identity_error():
    identity = Identity()
    with pytest.raises(TypeError):
        identity({"some": "value"})
