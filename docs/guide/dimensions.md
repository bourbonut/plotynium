# Dimensions

You can change the dimensions of your visualization through [`plot`](../api/plot.md) parameters.

```python hl_lines="16-21"
import plotynium as ply
from math import sin, pi
import random

random.seed(42)

data = [
    {
        "x_values": i / (4 * pi),
        "y_values": sin(i / (4 * pi)) + 0.5 * (random.random() - 0.5),
    }
    for i in range(100)
]

plot = ply.plot(
    width=928,
    height=500,
    margin_top=60,
    margin_left=120,
    margin_bottom=120,
    margin_right=60,
    marks=[ply.line(data, x="x_values", y="y_values")],
)

with open("plot.svg", "w") as file:
    file.write(str(plot))
```

![](../images/guide-dims.svg)
