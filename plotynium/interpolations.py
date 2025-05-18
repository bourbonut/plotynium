from enum import Enum

import detroit as d3


class Interpolation(Enum):
    """
    All available interpolations used mainly for color scheme
    """

    BLUES = d3.interpolate_blues
    BRBG = d3.interpolate_brbg
    BUGN = d3.interpolate_bugn
    BUPU = d3.interpolate_bupu
    CIVIDIS = d3.interpolate_cividis
    COOL = d3.interpolate_cool
    DEFAULT = d3.interpolate_cubehelix_default
    GNBU = d3.interpolate_gnbu
    GREENS = d3.interpolate_greens
    GREYS = d3.interpolate_greys
    INFERNO = d3.interpolate_inferno
    MAGMA = d3.interpolate_magma
    ORANGES = d3.interpolate_oranges
    ORRD = d3.interpolate_orrd
    PIYG = d3.interpolate_piyg
    PLASMA = d3.interpolate_plasma
    PRGN = d3.interpolate_prgn
    PUBU = d3.interpolate_pubu
    PUBUGN = d3.interpolate_pubugn
    PUOR = d3.interpolate_puor
    PURD = d3.interpolate_purd
    PURPLES = d3.interpolate_purples
    RAINBOW = d3.interpolate_rainbow
    RDBU = d3.interpolate_rdbu
    RDGY = d3.interpolate_rdgy
    RDPU = d3.interpolate_rdpu
    RDYLBU = d3.interpolate_rdylbu
    RDYLGN = d3.interpolate_rdylgn
    REDS = d3.interpolate_reds
    SINEBOW = d3.interpolate_sinebow
    SPECTRAL = d3.interpolate_spectral
    TURBO = d3.interpolate_turbo
    VIRIDIS = d3.interpolate_viridis
    WARM = d3.interpolate_warm
    YLGN = d3.interpolate_ylgn
    YLGNBU = d3.interpolate_ylgnbu
    YLORBR = d3.interpolate_ylorbr
    YLORRD = d3.interpolate_ylorrd
