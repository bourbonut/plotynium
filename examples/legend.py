import plotynium as ply

plot = ply.plot([ply.legend()], style={"font_family": "system-ui"})

with open("legend.svg", "w") as file:
    file.write(str(plot))
