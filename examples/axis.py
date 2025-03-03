import plotynium as plot

plot = plot.plot(
    margin_right=60,
    margin_top=40,
    marks=[
        plot.axis_x(label="my x label"),
        plot.axis_y(label="my y label"),
    ],
    # style={"color": "#e6edf3"},
)

with open("axis.svg", "w") as file:
    file.write(str(plot))
