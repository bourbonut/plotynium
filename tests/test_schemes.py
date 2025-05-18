import pytest

from plotynium.schemes import Scheme

ALL_SCHEMES = [
    Scheme.CATEGORY_10,
    Scheme.ACCENT,
    Scheme.DARK_2,
    Scheme.OBSERVABLE_10,
    Scheme.PAIRED,
    Scheme.PASTEL_1,
    Scheme.PASTEL_2,
    Scheme.SET_1,
    Scheme.SET_2,
    Scheme.SET_3,
    Scheme.TABLEAU_10,
]


def test_schemes_all_different():
    assert len(ALL_SCHEMES) == len(set(ALL_SCHEMES))


@pytest.mark.parametrize("scheme", ALL_SCHEMES)
def test_schemes_one_by_one(scheme):
    assert isinstance(scheme(0.5), str)
