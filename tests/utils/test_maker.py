from plotynium.utils.maker import Maker
import pytest

def test_abstract_maker():
    with pytest.raises(TypeError) as exc:
        Maker()

    assert "__call__" in str(exc.value)
    assert "__init__" in str(exc.value)
