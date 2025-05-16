# from plotynium.symbols import SymbolFill, SymbolStroke, symbol_legend
# from plotynium.interpolations import Interpolation
# import inspect
# import pytest
# import detroit as d3
# from detroit.selection.selection import Selection
#
# ALL_SYMBOL_FILL = [
#     SymbolFill.CIRCLE,
#     SymbolFill.CROSS,
#     SymbolFill.DIAMOND,
#     SymbolFill.SQUARE,
#     SymbolFill.STAR,
#     SymbolFill.TRIANGLE,
#     SymbolFill.WYE,
# ]
#
# ALL_SYMBOL_STROKE = [
#     SymbolStroke.ASTERISK,
#     SymbolStroke.CIRCLE,
#     SymbolStroke.DIAMOND,
#     SymbolStroke.PLUS,
#     SymbolStroke.SQUARE,
#     SymbolStroke.TIMES,
#     SymbolStroke.TRIANGLE,
# ]
#
# @pytest.mark.parametrize("all_symbols", [ALL_SYMBOL_FILL, ALL_SYMBOL_STROKE])
# def test_symbol_all_different(all_symbols):
#     assert len(all_symbols) == len(set(all_symbols))
#
# @pytest.mark.parametrize("symbol", ALL_SYMBOL_FILL + ALL_SYMBOL_STROKE)
# def test_symbol(symbol):
#     assert callable(symbol)
#     sign = inspect.signature(symbol)
#     assert list(sign.parameters.keys()) == ["context", "size"]
#
#
# def test_symbol_legend():
#     svg = d3.create("svg")
#     labels = ["a", "b", "c"]
#     margin_left = 10
#     margin_top = 20
#     scheme = Interpolation.TURBO
#
#     symbol_legend(svg, labels, margin_left, margin_top, scheme)
#
#     legend = svg.select("g.legend")
#     assert len(legend.nodes()) == 1
#     labels_groups = legend.select_all("g")
#     assert len(labels_groups.nodes()) == len(labels)
#     for node, label in zip(labels_groups, labels):
#         sel = Selection([[node]], [])
#         path = sel.select("path")
#         text = sel.select("text")
#         assert len(path.nodes()) == 1
#         assert len(text.nodes()) == 1
#
#         assert f">{label}<" in str(text)
