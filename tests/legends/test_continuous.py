from plotynium.legends import Legend
from tests.default_context import default_context
import detroit as d3


def test_continuous_legend():
    legend = Legend()

    svg = d3.create("svg")
    ctx = default_context(d3.scale_linear(), d3.scale_linear())
    legend.apply(svg, ctx)
    assert len(svg.select_all("rect").nodes()) == 105
    assert len(svg.select_all("path").nodes()) == 6
    assert len(svg.select_all("text").nodes()) == 6
