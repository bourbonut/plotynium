# Area mark

The [Area][plotynium.marks.AreaY] draws the region between a baseline \((x_1, y_1)\) and a topline \((x_2, y_2)\) as in area chart. \(x\) scale and \(y\) scale are quantitive or temporal.


![](../images/area.svg)

```python hl_lines="22-27"
import plotynium as plot
import polars as pl

URL = (
    "https://static.observableusercontent.com/files/de259092d525c13bd10926ea"
    "https://static.observableusercontent.com/files/de259092d525c13bd10926ea"
    "f7add45b15f2771a8b39bc541a5bba1e0206add4880eb1d876be8df469328a85243b7d8"
    "13a91feb8cc4966de582dc02e5f8609b7?response-content-disposition=attachme"
    "nt%3Bfilename*%3DUTF-8%27%27aapl.csv"
)

# Download data and prepare them
aapl = pl.read_csv(URL).select( # columns = ['date', 'close']
    pl.col("date").str.to_datetime("%Y-%m-%d"),
    pl.col("close"),
)

plot = plot.plot(
    width=928,
    height=500,
    marks=[
        plot.area_y(
            data=aapl.to_dicts(),
            x="date",
            y="close",
            fill="steelblue",
        )
    ],
    x={"grid": True, "nice": False},
)

with open("area.svg", "w") as file:
    file.write(str(plot))
```
