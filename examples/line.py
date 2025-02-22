import plotynium as plot
from plotynium.options import XOptions
import polars as pl

URL = "https://static.observableusercontent.com/files/de259092d525c13bd10926eaf7add45b15f2771a8b39bc541a5bba1e0206add4880eb1d876be8df469328a85243b7d813a91feb8cc4966de582dc02e5f8609b7?response-content-disposition=attachment%3Bfilename*%3DUTF-8%27%27aapl.csv"

aapl = pl.read_csv(URL).select(
    pl.col("date").str.to_datetime("%Y-%m-%d"),
    pl.col("close"),
)

plot = plot.plot(
    marks=[
        plot.line(data=aapl.to_dicts(), x="date", y="close", stroke="steelblue", stroke_width=1.5),
        plot.rule_y([0])
    ],
    width=928,
    height=500,
    x=XOptions(grid=True),
)

with open("line.svg", "w") as file:
    file.write(str(plot))
