from datetime import datetime
from collections.abc import Callable
from operator import itemgetter
from .scaler import Scaler

def domain(data: list, accessor: Callable) -> tuple[list, Scaler]:
    sample = accessor(data[0])
    if isinstance(sample, str):
        uniques = set()
        values = []
        for value in map(accessor, data):
            if value in uniques:
                continue
            uniques.add(value)
            values.append(value)
        return values, Scaler.BAND
    values = list(map(accessor, data))
    scaler_type = Scaler.TIME if isinstance(sample, datetime) else Scaler.CONTINOUS
    return [min(values), max(values)], scaler_type

def reduce(domains):
    mins = list(map(itemgetter(0), domains))
    maxs = list(map(itemgetter(1), domains))
    return [min(mins), max(maxs)]

def unify(domains):
    domains = set(map(tuple, domains))
    if len(domains) > 1:
        raise RuntimeError(f"Too many domains to deal with (found {domains}).")
    elif len(domains) == 0:
        raise ValueError("No domain found.")
    return domains.pop()
