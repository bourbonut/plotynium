import plotynium as ply

x = list(range(0, 21))
data = [
    {
        "x": xi,
        "y": pow(xi, i + 1),
        "label": (f"$y = x^{i + 1}$" if i > 0 else "$y = x$"),
    }
    for i in range(3) for xi in x
]

plot = ply.plot(
    marks=[ply.line(data, x="x", y="y", stroke="label")],
    color={"legend": True, "scheme": ply.Scheme.OBSERVABLE_10},
    y={"specifier": "~s"}
)

with open("figure.svg", "w") as file:
    file.write(str(plot))
