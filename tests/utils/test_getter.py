from plotynium.utils.getter import getter
from operator import itemgetter

def test_getter_callable():
    value = lambda d: d
    assert getter(value) == value

def test_getter_string():
    value = "value"
    assert getter(value)({"value": 10}) == 10

def test_getter_index():
    value = 0
    assert getter(value)([10]) == 10
