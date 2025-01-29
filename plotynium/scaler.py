from datetime import datetime
from enum import Enum, auto
from . import domain
import detroit as d3
from collections.abc import Callable

class Scaler(Enum):
    BAND = auto()
    CONTINOUS = auto()
    TIME = auto()


def determine_scaler(data: list, accessor: Callable):
    sample = accessor(data[0])
    if isinstance(sample, str):
        return Scaler.BAND
    elif isinstance(sample, datetime):
        return Scaler.TIME
    else:
        return Scaler.CONTINOUS


def reduce(scaler_types: list):
    scalers = set(scaler_types)
    if len(scalers) > 1:
        raise RuntimeError(f"Found different scalers {scalers}. Some marks cannot be associated between each other.")
    elif len(scalers) == 0:
        raise ValueError("Cannot identify scaler for marks.")
    return scalers.pop()


def make_scaler(
    scaler_types: list[Scaler],
    domains: list[list | tuple[float, float]],
    range_vals: list[tuple[int, int]],
    nice: bool = False,
):
    scaler_type = reduce(scaler_types)

    if scaler_type == Scaler.CONTINOUS:
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
        )
    else:
        raise ValueError(f"Undefined scaler (found {x_scaler_type})")

    if nice and scaler_type in [Scaler.CONTINOUS, Scaler.TIME]:
        scaler = scaler.nice()

    return scaler
