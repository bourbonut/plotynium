from datetime import datetime
from collections.abc import Callable
from operator import itemgetter

def domain(data: list, accessor: Callable) -> list:
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

def reduce(domains):
    domains = [domain for domain in domains if domain is not None]
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
