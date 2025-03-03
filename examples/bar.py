import plotynium as plot
from plotynium.options import SortOptions
import polars as pl

URL = "https://static.observableusercontent.com/files/09f63bb9ff086fef80717e2ea8c974f918a996d2bfa3d8773d3ae12753942c002d0dfab833d7bee1e0c9cd358cd3578c1cd0f9435595e76901508adc3964bbdc?response-content-disposition=attachment%3Bfilename*%3DUTF-8%27%27alphabet.csv"

alphabet = pl.read_csv(URL)

plot = plot.plot(
    width=928,
    height=500,
    marks=[
        plot.bar_y(
            data=alphabet.to_dicts(),
            x="letter",
            y="frequency",
            sort={"by": "frequency", "descending": True},
            fill="steelblue",
        )
    ],
    margin_left=60,
    style={"color": "#e6edf3"},
)

with open("bar.svg", "w") as file:
    file.write(str(plot))
