from plotynium.transformers import getter

def test_getter_callable():
    def value(d):
        return d
    assert getter(value) == value

def test_getter_string():
    value = "value"
    assert getter(value)({"value": 10}) == 10

def test_getter_index():
    value = 0
    assert getter(value)([10]) == 10
