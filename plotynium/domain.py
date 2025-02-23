from datetime import datetime
from collections.abc import Callable
from operator import itemgetter
from .types import T, Number, Data

def domain(data: list[T], accessor: Callable[[T], Data]) -> tuple[Number, Number] | list[str]:
    sample = accessor(data[0])
    if isinstance(sample, str): # Band case
        uniques = set()
        values = []
        for value in map(accessor, data):
            if value in uniques:
                continue
            uniques.add(value)
            values.append(value)
        return values
    values = list(map(accessor, data))
    return [min(values), max(values)]

def reduce(domains: list[tuple[Number, Number] | None]) -> tuple[Number, Number]:
    domains = [domain for domain in domains if domain is not None]
    mins = list(map(itemgetter(0), domains)) or [0.]
    maxs = list(map(itemgetter(1), domains)) or [1.]
    return [min(mins), max(maxs)]

def unify(domains: list[tuple[Number, Number] | None]) -> tuple[Number, Number]:
    domains = set(map(tuple, domains))
    if len(domains) > 1:
        raise RuntimeError(f"Too many domains to deal with (found {domains}).")
    elif len(domains) == 0:
        raise ValueError("No domain found.")
    return domains.pop()
