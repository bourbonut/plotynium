from detroit.types import Scaler

from .options import ColorOptions, StyleOptions, SymbolOptions, XOptions, YOptions
from .properties import CanvasProperties, LegendProperties, Margin
from .types import ColorScheme

__all__ = ["Context"]


class Context:
    """
    The `Context` holds all information shared to `Mark` objects and `Legend`
    object. These information are computed dimensions, options, scalers and
    labels.

    Parameters
    ----------
    canvas_properties : CanvasProperties
        Canvas properties (width, height and margin)
    legend_properties : LegendProperties
        Legend properties (width, height and margin)
    x_options : XOptions
        X axis options
    y_options : YOptions
        Y axis options
    color_options : ColorOptions
        Color options
    style_options : StyleOptions
        Style options
    symbol_options : SymbolOptions
        Symbol options
    x_scale : Scaler
        X scale from [`detroit`](https://detroit.readthedocs.io/en/latest/api/types.html#detroit.types.Scaler)
    y_scale : Scaler
        Y scale from [`detroit`](https://detroit.readthedocs.io/en/latest/api/types.html#detroit.types.Scaler)
    x_label : str | None
        X label
    y_label : str | None
        Y label
    """

    def __init__(
        self,
        canvas_properties: CanvasProperties,
        legend_properties: LegendProperties,
        x_options: XOptions,
        y_options: YOptions,
        color_options: ColorOptions,
        style_options: StyleOptions,
        symbol_options: SymbolOptions,
        x_scale: Scaler,
        y_scale: Scaler,
        x_label: str | None = None,
        y_label: str | None = None,
    ):
        self._canvas_properties = canvas_properties
        self._legend_properties = legend_properties

        self._x_options = x_options
        self._y_options = y_options
        self._color_options = color_options
        self._style_options = style_options
        self._symbol_options = symbol_options

        self._color_mapping = []
        self._symbol_mapping = []

        self._x = x_scale
        self._y = y_scale

    @property
    def x(self) -> Scaler:
        """
        Returns X scale.

        Returns
        -------
        Scaler
            X scale
        """
        return self._x

    @property
    def y(self) -> Scaler:
        """
        Returns Y scale.

        Returns
        -------
        Scaler
            Y scale
        """
        return self._y

    @property
    def x_label(self) -> str | None:
        """
        Returns X label.

        Returns
        -------
        str | None
            X label
        """
        return self._x_label

    @property
    def y_label(self) -> str | None:
        """
        Returns Y label.

        Returns
        -------
        str | None
            Y label
        """
        return self._y_label

    @property
    def width(self) -> int:
        """
        Returns width size of the canvas.

        Returns
        -------
        int
            Width size of the canvas
        """
        return self._canvas_properties.width

    @property
    def height(self) -> int:
        """
        Returns height size of the canvas.

        Returns
        -------
        int
            Height size of the canvas
        """
        return self._canvas_properties.height

    @property
    def margin(self) -> Margin:
        """
        Returns margin values of the canvas.

        Returns
        -------
        int
            Margin values of the canvas
        """
        return self._canvas_properties.margin

    @property
    def canvas_translate(self) -> str | None:
        """
        Returns the canvas translation value. For instance,
        `"translate(15, 12)"` and if `x` and `y` values of the translation
        equal zero, it returns `None`.

        Returns
        -------
        str | None
            Translation value of the canvas
        """
        return self._canvas_properties.translate

    @property
    def color(self) -> str:
        """
        Returns the color of the text.

        Returns
        -------
        str
            Text color value
        """
        return self._style_options.color

    @property
    def font_size(self) -> int:
        """
        Returns the font size.

        Returns
        -------
        int
            Font size value
        """
        return self._style_options.font_size

    @property
    def font_family(self) -> str:
        """
        Returns the font family.

        Returns
        -------
        str
            Font family value
        """
        return self._style_options.font_family

    @property
    def background(self) -> str:
        """
        Returns the background value.

        Returns
        -------
        str
            Background value
        """
        return self._style_options.background

    @property
    def color_scheme(self) -> ColorScheme:
        """
        Returns the color scheme value.

        Returns
        -------
        ColorScheme
            Color scheme value
        """
        return self._color_options.scheme

    @property
    def labels(self) -> dict[int, str]:
        """
        Returns the definition of user labels.

        Returns
        -------
        dict[int, str]
            Dictionary where keys are indices of labels and values are label
            values
        """
        return self._color_options.labels

    @property
    def legend_properties(self) -> LegendProperties:
        """
        Returns legend properties.

        Returns
        -------
        LegendProperties
            Legend properties.
        """
        return self._legend_properties

    @property
    def color_mapping(self) -> list[tuple[str, str]]:
        """
        Returns color mapping collected after the application of marks.

        Returns
        -------
        list[tuple[str, str]]
            List of pairs (label, color)
        """
        return self._color_mapping

    @property
    def symbol_mapping(self) -> list[tuple[str, str]]:
        """
        Returns symbol mapping collected after the application of marks.

        Returns
        -------
        list[tuple[str, str]]
            List of pairs (label, symbol path)
        """
        return self._symbol_mapping

    def update_color_mapping(self, *color_mappings: tuple[list[tuple[str, str]]]):
        """
        Sets the color mapping by prioritizing the longest color mapping list.

        Parameters
        ----------
        color_mappings : tuple[list[tuple[str, str]]]
            Several list of pairs (label, color)
        """
        color_mappings = [self._color_mapping] + list(color_mappings)
        self._color_mapping = max(color_mappings, key=len)

    def update_symbol_mapping(self, *symbol_mappings: tuple[list[tuple[str, str]]]):
        """
        Sets the symbol mapping by prioritizing the longest symbol mapping list.

        Parameters
        ----------
        symbol_mappings : tuple[list[tuple[str, str]]]
            Several list of pairs (label, symbol path)
        """
        symbol_mappings = [self._symbol_mapping] + list(symbol_mappings)
        self._symbol_mapping = max(symbol_mappings, key=len)
