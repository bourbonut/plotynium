from datetime import datetime, timedelta

import pytest
from detroit.scale.band import ScaleBand
from detroit.scale.linear import ScaleLinear
from detroit.scale.time import ScaleTime

from plotynium.scaler import ScalerType, determine_scaler, make_scaler, reduce

ALL_SCALER = [
    ScalerType.BAND,
    ScalerType.CONTINUOUS,
    ScalerType.TIME,
]


def test_scaler_all_different():
    assert len(ALL_SCALER) == len(set(ALL_SCALER))


@pytest.mark.parametrize(
    "data, accessor, expected",
    [
        [[(x, x * 2) for x in range(10)], (lambda d: d[0]), ScalerType.CONTINUOUS],
        [[(x, datetime.now()) for x in range(10)], (lambda d: d[1]), ScalerType.TIME],
        [[(v, i) for i, v in enumerate("aabbc")], (lambda d: d[0]), ScalerType.BAND],
    ],
)
def test_determine_scaler(data, accessor, expected):
    assert determine_scaler(data, accessor) == expected


def test_reduce_ok():
    assert reduce([ScalerType.BAND, ScalerType.BAND]) == ScalerType.BAND


def test_reduce_different():
    with pytest.raises(RuntimeError):
        reduce([ScalerType.CONTINUOUS, ScalerType.BAND])


def test_reduce_no_scaler_type():
    assert reduce([]) == ScalerType.CONTINUOUS


@pytest.mark.parametrize(
    "scaler_types, domains, range_vals, expected",
    [
        [[ScalerType.CONTINUOUS], [[0.0, 1.0]], [0.0, 1.0], ScaleLinear],
        [
            [ScalerType.TIME],
            [[datetime.now() - timedelta(seconds=10), datetime.now()]],
            [0.0, 1.0],
            ScaleTime,
        ],
        [[ScalerType.BAND], [["a", "b", "c"]], [0.0, 1.0], ScaleBand],
    ],
)
def test_make_scaler_ok(scaler_types, domains, range_vals, expected):
    assert isinstance(
        make_scaler(scaler_types, domains, range_vals, nice=False), expected
    )
    assert isinstance(
        make_scaler(scaler_types, domains, range_vals, nice=True), expected
    )


def test_make_scaler_error():
    with pytest.raises(ValueError):
        make_scaler(["bad_scaler"], [[0.0, 1.0]], [0.0, 1.0])
