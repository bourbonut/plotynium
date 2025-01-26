from collections.abc import Callable
from operator import itemgetter

def domain(data: list, accessor: Callable):
    values = list(map(accessor, data))
    return [min(values), max(values)]

def ordered_unique_domain(data: list, accessor: Callable):
    values = set(enumerate(map(accessor, data)))
    return [value for _, value in sorted(values, key=itemgetter(0))]

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
