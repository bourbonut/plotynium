from ..interpolations import Interpolation
from ..schemes import Scheme
from ..types import ColorScheme


def default_colorscheme(nb_labels: int) -> ColorScheme:
    """
    Returns the default color scheme given the number of labels. If there are
    too many labels, the color scheme is considered as *continuous* where as if
    there are equal or less than 10 labels, the color scheme is considered as
    *discrete*.

    Parameters
    ----------
    nb_labels : int
        Number of labels

    Returns
    -------
    ColorScheme
        Color scheme
    """
    return Interpolation.TURBO if nb_labels > 10 else Scheme.OBSERVABLE_10
