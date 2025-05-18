import pytest

from plotynium.domain import domain, reduce, unify


@pytest.mark.parametrize(
    "data, accessor, expected",
    [
        [[(x, x * 2) for x in range(10)], (lambda d: d[0]), [0, 9]],
        [[(x, x * 2) for x in range(10)], (lambda d: d[1]), [0, 18]],
        [[(v, i) for i, v in enumerate("aabbc")], (lambda d: d[0]), ["a", "b", "c"]],
    ],
)
def test_domain(data, accessor, expected):
    assert domain(data, accessor) == expected


@pytest.mark.parametrize(
    "domains, expected",
    [
        [[[0, 1], None, [10, 20], None, [-120, -20]], [-120, 20]],
        [[None] * 10, [0.0, 1.0]],
    ],
)
def test_reduce(domains, expected):
    assert reduce(domains) == expected


def test_unify_ok():
    assert unify([[0.0, 1.0], [0.0, 1.0]]) == (0.0, 1.0)


def test_unify_too_many():
    with pytest.raises(RuntimeError):
        unify([[0.0, 1.0], ["a", "b", "c"]])


def test_unify_no_domain():
    with pytest.raises(ValueError):
        unify([])
