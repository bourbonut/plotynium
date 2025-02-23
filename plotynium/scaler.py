from datetime import datetime
from enum import Enum, auto
from . import domain
import detroit as d3
from collections.abc import Callable

class Scaler(Enum):
    BAND = auto()
    CONTINUOUS = auto()
    TIME = auto()


def determine_scaler(data: list, accessor: Callable):
    sample = accessor(data[0])
    if isinstance(sample, str):
        return Scaler.BAND
    elif isinstance(sample, datetime):
        return Scaler.TIME
    else:
        return Scaler.CONTINUOUS


def reduce(scaler_types: list):
    scalers = set(scaler_types) - {None}
    if len(scalers) > 1:
        raise RuntimeError(f"Found different scalers {scalers}. Some marks cannot be associated between each other.")
    elif len(scalers) == 0:
        return Scaler.CONTINUOUS
    return scalers.pop()


def make_scaler(
    scaler_types: list[Scaler],
    domains: list[list | tuple[float, float]],
    range_vals: list[int | float],
    nice: bool = True,
):
    scaler_type = reduce(scaler_types)

    if scaler_type == Scaler.CONTINUOUS:
        scaler = (
            d3.scale_linear()
            .set_domain(domain.reduce(domains))
            .set_range(range_vals)
        )
    elif scaler_type == Scaler.TIME:
        scaler = (
            d3.scale_time()
            .set_domain(domain.reduce(domains))
            .set_range(range_vals)
        )
    elif scaler_type == Scaler.BAND:
        scaler = (
            d3.scale_band()
            .set_domain(domain.unify(domains))
            .set_range(range_vals)
            .set_padding(0.1)
        )
    else:
        raise ValueError(f"Undefined scaler (found {scaler_type})")

    if nice and scaler_type in [Scaler.CONTINUOUS, Scaler.TIME]:
        scaler = scaler.nice()

    return scaler
