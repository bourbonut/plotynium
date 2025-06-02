import random
from math import hypot

import plotynium as ply

data = [[random.random(), random.random()] for i in range(1000)]

scheme = ply.Scheme.OBSERVABLE_10
scheme(0)  # stores 0 in the scheme
scheme(1)  # stores 1 in the scheme

plot = ply.plot(
    width=500,
    height=500,
    margin_top=10,
    margin_left=30,
    margin_bottom=20,
    margin_right=10,
    marks=[ply.dot(data, stroke=lambda d: scheme(bool(hypot(*d) < 1)))],
    x={"nice": True},
    y={"nice": True},
    color={"legend": True, "labels": {0: "Inside", 1: "Outside"}},
    style={"color": "white"},
)

with open("pi.svg", "w") as file:
    file.write(str(plot))
