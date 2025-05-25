from plotynium.legends import Legend
from tests.default_context import default_context
import detroit as d3

def test_discrete_legend():
    colors = ("blue", "red", "green")
    legend = Legend(
        [(f"label_{i}", color) for i, color in enumerate(colors)]
    )

    svg = d3.create("svg")
    ctx = default_context(d3.scale_linear(), d3.scale_linear())
    legend.apply(svg, ctx)
    g = svg.select("g.legend").select_all("g")
    assert len(g.nodes()) == 3
    assert len(g.select_all("rect").nodes()) == 3
    assert len(g.select_all("text").nodes()) == 3
