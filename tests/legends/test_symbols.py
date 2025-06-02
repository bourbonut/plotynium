from plotynium.legends import Legend
from tests.default_context import default_context
import detroit as d3


def test_symbol_legend():
    colors = ("blue", "red", "green")
    symbols = d3.scale_ordinal(
        [f"label_{i}" for i in range(len(colors))], d3.SYMBOLS_STROKE
    )
    legend = Legend(
        [(f"label_{i}", color) for i, color in enumerate(colors)],
        [
            (f"label_{i}", d3.symbol(symbols(f"label_{i}"))())
            for i in range(len(colors))
        ],
    )

    svg = d3.create("svg")
    ctx = default_context(d3.scale_linear(), d3.scale_linear())
    legend.apply(svg, ctx)
    g = svg.select("g.legend").select_all("g")
    assert len(g.nodes()) == 3
    assert len(g.select_all("path").nodes()) == 3
    assert len(g.select_all("text").nodes()) == 3
