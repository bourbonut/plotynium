import polars as pl

import plotynium as ply

URL = "https://static.observableusercontent.com/files/1734c862dd51ef67930fef3dcd19e8184bb65c405683f55a085f97ca01c233713a53062c251fe0a6d72f93863fd5f714eadef3c9455b1b4f2ed90546cbc57b32?response-content-disposition=attachment%3Bfilename*%3DUTF-8%27%27gistemp.csv"

gistemp = pl.read_csv(URL).select(
    pl.col("Date").str.to_datetime("%Y-%m-%d"),
    pl.col("Anomaly"),
)

plot = ply.plot(
    marks=[
        ply.rule_y([0]),
        ply.dot(gistemp.to_dicts(), x="Date", y="Anomaly", stroke="Anomaly"),
    ],
    y={"grid": True, "specifier": "+f", "label": "Surface temperature anomaly (°C)"},
    color={
        "scheme": ply.Interpolation.RDBU,
        "legend": True,
    },
    margin_left=60,
)

with open("diverging.svg", "w") as file:
    file.write(str(plot))
