from collections.abc import Callable
from datetime import datetime
from enum import Enum, auto

import detroit as d3
from detroit.types import Scaler as D3Scaler

from .domain import reduce as domain_reduce
from .domain import unify
from .types import U, V


class Scaler(Enum):
    """
    All types of scalers
    """

    BAND = auto()
    CONTINUOUS = auto()
    TIME = auto()


def determine_scaler(data: list[U], accessor: Callable[[U], V]) -> Scaler:
    """
    Determine the scaler type given data.

    Parameters
    ----------
    data : list[U]
        Data
    accessor : Callable[[U], V]
        Function to access data for each element in `data`

    Returns
    -------
    Scaler
        Scaler type
    """
    sample = accessor(data[0])
    if isinstance(sample, str):
        return Scaler.BAND
    elif isinstance(sample, datetime):
        return Scaler.TIME
    else:
        return Scaler.CONTINUOUS


def reduce(scaler_types: list[Scaler | None]) -> Scaler:
    """
    Checks if all `scaler_types` are the same and returns a unique scaler type
    if it is the case.

    Parameters
    ----------
    scaler_types : list[Scaler | None]
        List of scaler types

    Returns
    -------
    Scaler
        Unique scaler type
    """
    scalers = set(scaler_types) - {None}
    if len(scalers) > 1:
        raise RuntimeError(
            f"Found different scalers {scalers}. Some marks cannot be"
            "associated between each other."
        )
    elif len(scalers) == 0:
        return Scaler.CONTINUOUS
    return scalers.pop()


def determine_label(labels: list[str | None]) -> str | None:
    """
    Reduces a list of labels into an unique one by checking consistency between
    labels. For instance, if there are different labels, the function will
    return `None`. However, if only the same label in the given list was found,
    it is returned by the function.

    Parameters
    ----------
    labels : list[str | None]
        List of labels defined as `str` or undefined as `None`

    Returns
    -------
    str | None
        Unique label from the given list or undefined label as `None`
    """
    labels = set(labels) - {None}
    if len(labels) == 1:
        if label := labels.pop():
            return label


def make_scaler(
    scaler_types: list[Scaler | None],
    domains: list[list | tuple[float, float]],
    range_vals: list[int | float],
    nice: bool = True,
) -> D3Scaler:
    """
    Returns a scaler object from `detroit`.

    Parameters
    ----------
    scaler_types : list[Scaler | None]
        Scaler types collected in marks
    domains : list[list | tuple[float, float]]
        Domains collected in marks
    range_vals : list[int | float]
        Range values collected in marks
    nice : bool
        `True` to make the scaler's domain nicer

    Returns
    -------
    D3Scaler
        [`ScaleLinear`](https://detroit.readthedocs.io/en/latest/api/scale/linear.html#detroit.scale.linear.ScaleLinear)
        or
        [`ScaleTime`](https://detroit.readthedocs.io/en/latest/api/scale/time.html#detroit.scale.time.ScaleTime)
        or
        [`ScaleBand`](https://detroit.readthedocs.io/en/latest/api/scale/band.html#detroit.scale.band.ScaleBand)
    """
    scaler_type = reduce(scaler_types)

    if scaler_type == Scaler.CONTINUOUS:
        scaler = (
            d3.scale_linear().set_domain(domain_reduce(domains)).set_range(range_vals)
        )
    elif scaler_type == Scaler.TIME:
        scaler = (
            d3.scale_time().set_domain(domain_reduce(domains)).set_range(range_vals)
        )
    elif scaler_type == Scaler.BAND:
        scaler = (
            d3.scale_band()
            .set_domain(unify(domains))
            .set_range(range_vals)
            .set_padding(0.1)
        )
    else:
        raise ValueError(f"Undefined scaler (found {scaler_type})")

    if nice and scaler_type in [Scaler.CONTINUOUS, Scaler.TIME]:
        scaler = scaler.nice()

    return scaler
