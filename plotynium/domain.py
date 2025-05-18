from collections.abc import Callable
from operator import itemgetter

from .types import Data, Number, T


def domain(
    data: list[T], accessor: Callable[[T], Data]
) -> tuple[Number, Number] | list[str]:
    """
    Generates a domain given data and an accessor function

    Parameters
    ----------
    data : list[T]
        Generic list of data
    accessor : Callable[[T], Data]
        Accessor function for extracting data (`str`, `float` or `int`)

    Returns
    -------
    tuple[Number, Number] | list[str]
        Domain defined by (min, max) when data are `float` or `int` or defined by
        a list of `str` when data are `str`
    """
    sample = accessor(data[0])
    if isinstance(sample, str):  # Band case
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
    """
    Reduces multiple domains defined as (min, max) into an unique one

    Parameters
    ----------
    domains : list[tuple[Number, Number] | None]
        List of domains (min, max) or undefined ones (i.e. `None`)

    Returns
    -------
    tuple[Number, Number]
        Domain (min, max) deduced from given domains; default `[0., 1.]`
    """
    domains = [domain for domain in domains if domain is not None]
    mins = list(map(itemgetter(0), domains)) or [0.0]
    maxs = list(map(itemgetter(1), domains)) or [1.0]
    return [min(mins), max(maxs)]


def unify(domains: list[tuple[Number, Number] | None]) -> tuple[Number, Number]:
    """
    Returns the consistent domain when it is possible. For instance, if there are too
    many different domains, the returned value will be `None`. However, if there is
    only one repeated domain in the given list, it will be returned by the function.

    Parameters
    ----------
    domains : list[tuple[Number, Number] | None]
        List of domains (min, max) or undefined ones (i.e. `None`)

    Returns
    -------
    tuple[Number, Number]
        Domain

    Raises
    ------
    RuntimeError
        When there are too many different domains
    ValueError
        When no domain was found
    """
    domains = set(map(tuple, domains))
    if len(domains) > 1:
        raise RuntimeError(f"Too many domains to deal with (found {domains}).")
    elif len(domains) == 0:
        raise ValueError("No domain found.")
    return domains.pop()
