import plotynium as ply
import polars as pl

URL = "https://static.observableusercontent.com/files/de259092d525c13bd10926eaf7add45b15f2771a8b39bc541a5bba1e0206add4880eb1d876be8df469328a85243b7d813a91feb8cc4966de582dc02e5f8609b7?response-content-disposition=attachment%3Bfilename*%3DUTF-8%27%27aapl.csv"

aapl = pl.read_csv(URL).select(
    pl.col("date").str.to_datetime("%Y-%m-%d"),
    pl.col("close"),
)

plot = ply.plot(
    width=928,
    height=500,
    marks=[
        ply.line(data=aapl.to_dicts(), x="date", y="close", stroke="steelblue", stroke_width=1.5),
        ply.rule_y([0], stroke="#e6edf3")
    ],
    x={"grid": True},
    style={"color": "#e6edf3"},
)

with open("line.svg", "w") as file:
    file.write(str(plot))
