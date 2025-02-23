from datetime import datetime
from enum import Enum, auto
from collections.abc import Callable

from .domain import reduce as domain_reduce, unify

import detroit as d3
from detroit.scale.band import ScaleBand
from detroit.scale.time import Calendar
from detroit.scale.linear import ScaleLinear

class Scaler(Enum):
    BAND = auto()
    CONTINUOUS = auto()
    TIME = auto()


def determine_scaler(data: list, accessor: Callable) -> Scaler:
    sample = accessor(data[0])
    if isinstance(sample, str):
        return Scaler.BAND
    elif isinstance(sample, datetime):
        return Scaler.TIME
    else:
        return Scaler.CONTINUOUS


def reduce(scaler_types: list[Scaler | None]) -> Scaler:
    scalers = set(scaler_types) - {None}
    if len(scalers) > 1:
        raise RuntimeError(f"Found different scalers {scalers}. Some marks cannot be associated between each other.")
    elif len(scalers) == 0:
        return Scaler.CONTINUOUS
    return scalers.pop()


def make_scaler(
    scaler_types: list[Scaler | None],
    domains: list[list | tuple[float, float]],
    range_vals: list[int | float],
    nice: bool = True,
) -> Calendar | ScaleLinear | ScaleBand:
    scaler_type = reduce(scaler_types)

    if scaler_type == Scaler.CONTINUOUS:
        scaler = (
            d3.scale_linear()
            .set_domain(domain_reduce(domains))
            .set_range(range_vals)
        )
    elif scaler_type == Scaler.TIME:
        scaler = (
            d3.scale_time()
            .set_domain(domain_reduce(domains))
            .set_range(range_vals)
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
