import random
from math import hypot

import plotynium as ply

data = [[random.random(), random.random()] for i in range(1000)]

scheme = ply.Scheme.OBSERVABLE_10

plot = ply.plot(
    width=500,
    height=500,
    margin_top=10,
    margin_left=30,
    margin_bottom=20,
    margin_right=10,
    marks=[ply.dot(data, stroke=lambda d: scheme(bool(hypot(*d) < 1)))],
    # color={"legend": True},
    x={"nice": True},
    y={"nice": True},
    color={"legend": True, "labels": {0: "Inside", 1: "Outside"}},
)

with open("pi.svg", "w") as file:
    file.write(str(plot))
