from plotynium.colors import color_legend
from plotynium.interpolations import Interpolation
import detroit as d3
from detroit.selection.selection import Selection

def test_color_legend():
    svg = d3.create("svg")
    labels = ["a", "b", "c"]
    margin_left = 10
    margin_top = 20
    scheme = Interpolation.TURBO
    font_size = 20

    color_legend(svg, labels, margin_left, margin_top, scheme)

    legend = svg.select("g.legend")
    assert len(legend.nodes()) == 1
    labels_groups = legend.select_all("g")
    assert len(labels_groups.nodes()) == len(labels)
    for node, label in zip(labels_groups, labels):
        sel = Selection([[node]], [])
        path = sel.select("rect")
        text = sel.select("text")
        assert len(path.nodes()) == 1
        assert len(text.nodes()) == 1

        assert f">{label}<" in str(text)
