from collections.abc import Callable
from operator import itemgetter

def domain(data: list, accessor: Callable):
    values = list(map(accessor, data))
    return [min(values), max(values)]

def reduce(domains):
    mins = list(map(itemgetter(0), domains))
    maxs = list(map(itemgetter(1), domains))
    return [min(mins), max(maxs)]
