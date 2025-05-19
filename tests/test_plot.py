import pytest
from detroit.selection.selection import Selection

from plotynium.interpolations import Interpolation
from plotynium.marks.area import AreaY
from plotynium.marks.bar import BarY
from plotynium.marks.dot import Dot
from plotynium.marks.grid import GridX, GridY
from plotynium.marks.line import Line
from plotynium.marks.rule import RuleY
from plotynium.plot import plot


def test_plot_default():
    svg = plot([])
    assert isinstance(svg, Selection)
    g = svg.select_all("g.canvas").select_all("g")
    assert len(g.nodes()) == 4


def test_plot_specific_arguments():
    svg = plot(
        [],
        width=1200,
        height=800,
        margin_top=20,
        margin_right=20,
        margin_left=60,
        margin_bottom=60,
        grid=True,
        x={"nice": True, "label": "x label"},
        y={"nice": False, "label": "y label"},
        color={"scheme": Interpolation.SINEBOW},
        style={"background": "black", "color": "white"},
        symbol={"legend": True},
    )
    assert isinstance(svg, Selection)
    string = str(svg)
    assert ">x label<" in string
    assert ">y label<" in string
    assert "white" in string
    assert "black" in string


@pytest.mark.parametrize(
    "mark",
    [
        Line([[x, y] for x, y in zip(range(11), range(11))]),
        GridX(),
        GridY(),
        AreaY([[x, y] for x, y in zip(range(11), range(11))]),
        Dot([[x, y] for x, y in zip(range(11), range(11))]),
        BarY([[x, y] for x, y in zip("aaabbbcccdd", range(11))]),
        RuleY([0, 1]),
    ],
)
def test_plot_line(mark):
    svg = plot([mark])
    assert isinstance(svg, Selection)
