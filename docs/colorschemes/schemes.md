# From `Scheme`

## Usage

[`Scheme`][plotynium.schemes.Scheme] is usually used for [`ColorOptions`][plotynium.options.ColorOptions].

=== "From `dict`"

    ```python
    import plotynium as ply

    plot = ply.plot(
        marks=[...],
        color={"scheme": ply.Scheme.ACCENT},
    )
    ```

=== "With `ColorOptions`"

    ```python
    import plotynium as ply

    plot = ply.plot(
        marks=[...],
        color=ply.ColorOptions(scheme=ply.Scheme.ACCENT)
    )
    ```

## Available schemes

`Scheme.ACCENT`

![](../images/schemes/discrete_scheme_accent.png)

`Scheme.CATEGORY_10`

![](../images/schemes/discrete_scheme_category_10.png)

`Scheme.DARK_2`

![](../images/schemes/discrete_scheme_dark_2.png)

`Scheme.OBSERVABLE_10`

![](../images/schemes/discrete_scheme_observable_10.png)

`Scheme.PAIRED`

![](../images/schemes/discrete_scheme_paired.png)

`Scheme.PASTEL_1`

![](../images/schemes/discrete_scheme_pastel_1.png)

`Scheme.PASTEL_2`

![](../images/schemes/discrete_scheme_pastel_2.png)

`Scheme.SET_1`

![](../images/schemes/discrete_scheme_set_1.png)

`Scheme.SET_2`

![](../images/schemes/discrete_scheme_set_2.png)

`Scheme.SET_3`

![](../images/schemes/discrete_scheme_set_3.png)

`Scheme.TABLEAU_10`

![](../images/schemes/discrete_scheme_tableau_10.png)
