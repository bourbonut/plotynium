import detroit as d3


class Scheme:
    """
    All available schemes for color scheme
    """

    CATEGORY_10 = d3.scale_ordinal(d3.SCHEME_CATEGORY_10)
    ACCENT = d3.scale_ordinal(d3.SCHEME_ACCENT)
    DARK_2 = d3.scale_ordinal(d3.SCHEME_DARK_2)
    OBSERVABLE_10 = d3.scale_ordinal(d3.SCHEME_OBSERVABLE_10)
    PAIRED = d3.scale_ordinal(d3.SCHEME_PAIRED)
    PASTEL_1 = d3.scale_ordinal(d3.SCHEME_PASTEL_1)
    PASTEL_2 = d3.scale_ordinal(d3.SCHEME_PASTEL_2)
    SET_1 = d3.scale_ordinal(d3.SCHEME_SET_1)
    SET_2 = d3.scale_ordinal(d3.SCHEME_SET_2)
    SET_3 = d3.scale_ordinal(d3.SCHEME_SET_3)
    TABLEAU_10 = d3.scale_ordinal(d3.SCHEME_TABLEAU_10)
