import pytest

from plotynium.interpolations import Interpolation

ALL_INTERPOLATIONS = [
    Interpolation.BLUES,
    Interpolation.BRBG,
    Interpolation.BUGN,
    Interpolation.BUPU,
    Interpolation.CIVIDIS,
    Interpolation.COOL,
    Interpolation.DEFAULT,
    Interpolation.GNBU,
    Interpolation.GREENS,
    Interpolation.GREYS,
    Interpolation.INFERNO,
    Interpolation.MAGMA,
    Interpolation.ORANGES,
    Interpolation.ORRD,
    Interpolation.PIYG,
    Interpolation.PLASMA,
    Interpolation.PRGN,
    Interpolation.PUBU,
    Interpolation.PUBUGN,
    Interpolation.PUOR,
    Interpolation.PURD,
    Interpolation.PURPLES,
    Interpolation.RAINBOW,
    Interpolation.RDBU,
    Interpolation.RDGY,
    Interpolation.RDPU,
    Interpolation.RDYLBU,
    Interpolation.RDYLGN,
    Interpolation.REDS,
    Interpolation.SINEBOW,
    Interpolation.SPECTRAL,
    Interpolation.TURBO,
    Interpolation.VIRIDIS,
    Interpolation.WARM,
    Interpolation.YLGN,
    Interpolation.YLGNBU,
    Interpolation.YLORBR,
    Interpolation.YLORRD,
]


def test_interpolations_all_different():
    assert len(ALL_INTERPOLATIONS) == len(set(ALL_INTERPOLATIONS))


@pytest.mark.parametrize("interpolation", ALL_INTERPOLATIONS)
def test_interpolations_one_by_one(interpolation):
    assert isinstance(interpolation(0.5), str)
