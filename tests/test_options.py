import pytest

from plotynium.interpolations import Interpolation
from plotynium.options import (
    ColorOptions,
    SortOptions,
    StyleOptions,
    SymbolOptions,
    XOptions,
    YOptions,
    init_options,
)


def test_color_options_default():
    color_options = ColorOptions()
    assert color_options.scheme is None
    assert color_options.legend is False


def test_color_options_new():
    color_options = ColorOptions.new({"scheme": Interpolation.SINEBOW, "legend": True})
    assert color_options.scheme == Interpolation.SINEBOW
    assert color_options.legend is True


def test_symbol_options_default():
    symbol_options = SymbolOptions()
    assert symbol_options.legend is False


def test_symbol_options_new():
    symbol_options = SymbolOptions.new({"legend": True})
    assert symbol_options.legend is True


def test_style_options_default():
    style_options = StyleOptions()
    assert style_options.background == "none"
    assert style_options.color == "black"
    assert style_options.font_size == 12
    assert style_options.font_family == "sans-serif"


def test_style_options_new():
    style_options = StyleOptions.new(
        {
            "background": "black",
            "color": "white",
            "font_size": 20,
            "font_family": "Hack",
        }
    )
    assert style_options.background == "black"
    assert style_options.color == "white"
    assert style_options.font_size == 20
    assert style_options.font_family == "Hack"


def test_sort_options_default():
    sort_options = SortOptions()
    assert sort_options.by == ""
    assert sort_options.descending is False


def test_sort_options_new():
    sort_options = SortOptions.new(
        {
            "by": "mean",
            "descending": True,
        }
    )
    assert sort_options.by == "mean"
    assert sort_options.descending is True


def test_x_options_default():
    x_options = XOptions()
    assert x_options.nice is False
    assert x_options.grid is False
    assert x_options.label is None


def test_x_options_new():
    x_options = XOptions.new(
        {
            "nice": True,
            "grid": True,
            "label": "x_label",
        }
    )
    assert x_options.nice is True
    assert x_options.grid is True
    assert x_options.label == "x_label"


def test_y_options_default():
    y_options = YOptions()
    assert y_options.nice is True
    assert y_options.grid is False
    assert y_options.label is None


def test_y_options_new():
    y_options = YOptions.new(
        {
            "nice": False,
            "grid": True,
            "label": "y_label",
        }
    )
    assert y_options.nice is False
    assert y_options.grid is True
    assert y_options.label == "y_label"


def test_init_options_from_dict():
    color_values = {"scheme": Interpolation.SINEBOW}
    color_options = init_options(color_values, ColorOptions)
    assert color_options.scheme == Interpolation.SINEBOW


def test_init_options_from_class():
    color_values = ColorOptions(scheme=Interpolation.SINEBOW)
    color_options = init_options(color_values, ColorOptions)
    assert color_options.scheme == Interpolation.SINEBOW


@pytest.mark.parametrize(
    "class_",
    [ColorOptions, SymbolOptions, StyleOptions, SortOptions, XOptions, YOptions],
)
def test_init_options_none(class_):
    assert init_options(None, class_) == class_()
