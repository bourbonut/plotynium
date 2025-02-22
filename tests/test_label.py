from plotynium.label import reduce
import pytest

@pytest.mark.parametrize(
    "labels, expected",
    [
        [["x_label_1"], "x_label_1"],
        [["x_label_1", "x_label_2"], None],
        [[None], None],
    ]
)
def test_reduce(labels, expected):
    assert reduce(labels) == expected
