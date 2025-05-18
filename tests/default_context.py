from plotynium.context import Context
from plotynium.options import (
    ColorOptions,
    StyleOptions,
    SymbolOptions,
    XOptions,
    YOptions,
)
from plotynium.properties import CanvasProperties, LegendProperties


def default_context(x_scale, y_scale, canvas_properties=None):
    return Context(
        canvas_properties or CanvasProperties(),
        LegendProperties(),
        XOptions(),
        YOptions(),
        ColorOptions(),
        StyleOptions(),
        SymbolOptions(),
        x_scale,
        y_scale,
    )
