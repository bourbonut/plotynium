from plotynium.scaler import Scaler, determine_scaler, reduce, make_scaler
from datetime import datetime, timedelta
from detroit.scale.band import ScaleBand
from detroit.scale.linear import ScaleLinear
from detroit.scale.time import Calendar
import pytest

ALL_SCALER = [
    Scaler.BAND,
    Scaler.CONTINOUS,
    Scaler.TIME,
]

def test_scaler_all_different():
    assert len(ALL_SCALER) == len(set(ALL_SCALER))


@pytest.mark.parametrize(
    "data, accessor, expected",
    [
        [[(x, x * 2) for x in range(10)], (lambda d: d[0]), Scaler.CONTINOUS],
        [[(x, datetime.now()) for x in range(10)], (lambda d: d[1]), Scaler.TIME],
        [[(v, i) for i, v in enumerate("aabbc")], (lambda d: d[0]), Scaler.BAND],
    ]
)
def test_determine_scaler(data, accessor, expected):
    assert determine_scaler(data, accessor) == expected

def test_reduce_ok():
    assert reduce([Scaler.BAND, Scaler.BAND]) == Scaler.BAND

def test_reduce_different():
    with pytest.raises(RuntimeError):
        reduce([Scaler.CONTINOUS, Scaler.BAND])

def test_reduce_no_scaler_type():
    assert reduce([]) == Scaler.CONTINOUS


@pytest.mark.parametrize(
    "scaler_types, domains, range_vals, expected",
    [
        [[Scaler.CONTINOUS], [[0., 1.]], [0., 1.], ScaleLinear],
        [[Scaler.TIME], [[datetime.now() - timedelta(seconds=10), datetime.now()]], [0., 1.], Calendar],
        [[Scaler.BAND], [["a", "b", "c"]], [0., 1.], ScaleBand],
    ]
)
def test_make_scaler_ok(scaler_types, domains, range_vals, expected):
    assert isinstance(make_scaler(scaler_types, domains, range_vals, nice=False), expected)
    assert isinstance(make_scaler(scaler_types, domains, range_vals, nice=True), expected)

def test_make_scaler_error():
    with pytest.raises(ValueError):
        make_scaler(["bad_scaler"], [[0., 1.]], [0., 1.])
