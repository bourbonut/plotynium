from __future__ import annotations

from collections.abc import Callable
from datetime import MAXYEAR, MINYEAR, datetime
from operator import itemgetter
from typing import Any

from .common import UniqueVariant, unique
from .scaler_type import ScalerType
from .types import T


class Domain:
    """
    Domain definition

    Parameters
    ----------
    values : list[int | float | str | datetime]
        Values of the domain
    scaler_type : ScalerType
        Scaler type
    """

    __slots__ = "values", "scaler_type"

    def __init__(
        self, values: list[int | float | str | datetime], scaler_type: ScalerType
    ):
        self.values = values
        self.type = scaler_type

    @classmethod
    def from_data(
        cls,
        data: list[T],
        accessor: Callable[[T], int | float | str | datetime] | None = None,
    ) -> Domain:
        """
        Generates a domain given the specified scaler type, an array of data and an
        accessor function.

        Parameters
        ----------
        scaler_type : ScalerType
            Scaler Type
        data : list[T]
            Generic list of data
        accessor : Callable[[T], int | float | str | datetime]
            Accessor function for extracting data (`str`, `float` or `int`)

        Returns
        -------
        Domain
            Domain
        """
        scaler_type = ScalerType.from_data(data, accessor)
        match scaler_type:
            case ScalerType.BAND:
                uniques = set()
                values = []
                iterable = data if accessor is None else map(accessor, data)
                for value in iterable:
                    if value in uniques:
                        continue
                    uniques.add(value)
                    values.append(value)
                return Domain(values, scaler_type)
            case ScalerType.CONTINUOUS | ScalerType.TIME:
                values = data if accessor is None else list(map(accessor, data))
                return Domain([min(values), max(values)], scaler_type)
            case ScalerType.UNKNOWN:
                raise RuntimeError("Unknown scaler")
        raise NotImplementedError(f"Scaler type {scaler_type}")

    @classmethod
    def reduce(cls, domains: list[Domain]) -> Domain:
        """
        Reduces multiple domains defined as (min, max) into an unique one

        Parameters
        ----------
        domains : list[Domain]
            List of domains (min, max) or undefined ones (i.e. `None`)

        Returns
        -------
        Domain
            Domain (min, max) deduced from given domains.
        """
        scaler_type, unique_variant = unique(domain.type for domain in domains)
        match unique_variant:
            case UniqueVariant.UNIQUE_VALUE:
                values = [domain.values for domain in domains]
                match scaler_type:
                    case ScalerType.CONTINUOUS:
                        mins = list(map(itemgetter(0), values)) or [0.0]
                        maxs = list(map(itemgetter(1), values)) or [1.0]
                        return cls([min(mins), max(maxs)], ScalerType.CONTINUOUS)
                    case ScalerType.TIME:
                        mins = list(map(itemgetter(0), values)) or [MINYEAR]
                        maxs = list(map(itemgetter(1), values)) or [MAXYEAR]
                        return cls([min(mins), max(maxs)], ScalerType.TIME)
                    case ScalerType.BAND:
                        unique_value, unique_variant = unique(values)
                        match unique_variant:
                            case UniqueVariant.UNIQUE_VALUE:
                                return cls(unique_value, ScalerType.BAND)  # type: ignore
                            case UniqueVariant.NO_VALUE:
                                raise RuntimeError("Undefined domain values")
                            case UniqueVariant.MULTIPLE_VALUES:
                                raise RuntimeError(
                                    "Multiple domain values found with scaler type band."
                                )
                    case ScalerType.UNKNOWN:
                        raise RuntimeError("Scaler type is undefined.")
            case UniqueVariant.NO_VALUE:
                raise RuntimeError("Scaler type is undefined.")
            case UniqueVariant.MULTIPLE_VALUES:
                raise RuntimeError(
                    f"Multiple scaler types has been found ({scaler_type})"
                )
        raise RuntimeError("Unreachable code.")
