from plotynium.legends import Legend
from plotynium.transformers import Constant
import detroit as d3

def test_init_legend():
    legend = Legend()

    # Mark attributes
    assert legend.x_label is None
    assert legend.y_label is None
    assert legend.x_domain is None
    assert legend.y_domain is None
    assert legend.x_scaler_type is None
    assert legend.y_scaler_type is None

    # Other attributes
    assert legend._color_mapping == [(str(x), "none") for x in d3.ticks(0, 1, 10)]
    assert legend._symbol_mapping == []
    assert legend._scheme is None
    assert legend._square_size == 15
    assert legend._symbol_size == 5
    assert isinstance(legend._fill, Constant)
    assert legend._fill("unknown") == "currentColor"
    assert legend._fill_opacity == 1.
    assert isinstance(legend._stroke, Constant)
    assert legend._stroke("unknown") == "currentColor"
    assert legend._stroke_opacity == 1.
    assert legend._stroke_width == 1.
    assert legend._font_size == 12
    assert legend.properties.width == 240
    assert legend.properties.height == 50
    assert legend.properties.margin.top == 21
    assert legend.properties.margin.left == 15
    assert legend.properties.margin.bottom == 21
    assert legend.properties.margin.right == 15
