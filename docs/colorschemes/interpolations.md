# From `Interpolation`

## Usage

[`Interpolation`][plotynium.interpolations.Interpolation] is usually used for [`ColorOptions`][plotynium.options.ColorOptions].

=== "From `dict`"

    ```python
    import plotynium as ply

    plot = ply.plot(
        marks=[...],
        color={"scheme": ply.Interpolation.MAGMA},
    )
    ```

=== "With `ColorOptions`"

    ```python
    import plotynium as ply

    plot = ply.plot(
        marks=[...],
        color=ply.ColorOptions(scheme=ply.Interpolation.MAGMA)
    )
    ```

## Available interpolations

`Interpolation.BLUES`

![](../images/interpolations/scheme_blues.png)

`Interpolation.BRBG`

![](../images/interpolations/scheme_brbg.png)

`Interpolation.BUGN`

![](../images/interpolations/scheme_bugn.png)

`Interpolation.BUPU`

![](../images/interpolations/scheme_bupu.png)

`Interpolation.CIVIDIS`

![](../images/interpolations/scheme_cividis.png)

`Interpolation.COOL`

![](../images/interpolations/scheme_cool.png)

`Interpolation.GNBU`

![](../images/interpolations/scheme_gnbu.png)

`Interpolation.GREENS`

![](../images/interpolations/scheme_greens.png)

`Interpolation.GREYS`

![](../images/interpolations/scheme_greys.png)

`Interpolation.INFERNO`

![](../images/interpolations/scheme_inferno.png)

`Interpolation.MAGMA`

![](../images/interpolations/scheme_magma.png)

`Interpolation.ORANGES`

![](../images/interpolations/scheme_oranges.png)

`Interpolation.ORRD`

![](../images/interpolations/scheme_orrd.png)

`Interpolation.PIYG`

![](../images/interpolations/scheme_piyg.png)

`Interpolation.PLASMA`

![](../images/interpolations/scheme_plasma.png)

`Interpolation.PRGN`

![](../images/interpolations/scheme_prgn.png)

`Interpolation.PUBU`

![](../images/interpolations/scheme_pubu.png)

`Interpolation.PUBUGN`

![](../images/interpolations/scheme_pubugn.png)

`Interpolation.PUOR`

![](../images/interpolations/scheme_puor.png)

`Interpolation.PURD`

![](../images/interpolations/scheme_purd.png)

`Interpolation.PURPLES`

![](../images/interpolations/scheme_purples.png)

`Interpolation.RAINBOW`

![](../images/interpolations/scheme_rainbow.png)

`Interpolation.RDBU`

![](../images/interpolations/scheme_rdbu.png)

`Interpolation.RDGY`

![](../images/interpolations/scheme_rdgy.png)

`Interpolation.RDPU`

![](../images/interpolations/scheme_rdpu.png)

`Interpolation.RDYLBU`

![](../images/interpolations/scheme_rdylbu.png)

`Interpolation.RDYLGN`

![](../images/interpolations/scheme_rdylgn.png)

`Interpolation.REDS`

![](../images/interpolations/scheme_reds.png)

`Interpolation.SINEBOW`

![](../images/interpolations/scheme_sinebow.png)

`Interpolation.SPECTRAL`

![](../images/interpolations/scheme_spectral.png)

`Interpolation.TURBO`

![](../images/interpolations/scheme_turbo.png)

`Interpolation.VIRIDIS`

![](../images/interpolations/scheme_viridis.png)

`Interpolation.WARM`

![](../images/interpolations/scheme_warm.png)

`Interpolation.YLGN`

![](../images/interpolations/scheme_ylgn.png)

`Interpolation.YLGNBU`

![](../images/interpolations/scheme_ylgnbu.png)

`Interpolation.YLORBR`

![](../images/interpolations/scheme_ylorbr.png)

`Interpolation.YLORRD`

![](../images/interpolations/scheme_ylorrd.png)
