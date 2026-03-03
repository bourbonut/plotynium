from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from enum import Enum, auto

from .types import T


class ScalerType(Enum):
    """
    All types of scalers
    """

    BAND = auto()
    CONTINUOUS = auto()
    TIME = auto()
    UNKNOWN = auto()

    @classmethod
    def from_data(
        cls,
        data: list[T],
        accessor: Callable[[T], int | float | str | datetime] | None = None,
    ) -> ScalerType:
        """
        Determine the scaler type given data.

        Parameters
        ----------
        data : list[T]
            Data
        accessor : Callable[[T], int | float | str | datetime] | None
            Function to access data for each element in `data`

        Returns
        -------
        Scaler
            Scaler type
        """
        sample = data[0] if accessor is None else accessor(data[0])
        if isinstance(sample, str):
            return cls.BAND
        elif isinstance(sample, datetime):
            return cls.TIME
        elif isinstance(sample, (float, int)):
            return cls.CONTINUOUS
        else:
            return cls.UNKNOWN
