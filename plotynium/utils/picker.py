from collections import OrderedDict
from ..types import T
from typing import Generic

class LegendPicker(Generic[T]):

    def __init__(self):
        self._labels: dict[int, str] = labels or {}
        self._indices: dict[T, int] = {}
        self._groups: dict[int, T] = {}

    def __call__(self, value: T) -> T:
        index = self._indices.setdefault(value, len(self._indices))
        self._groups[index] = result
        return value

    def __getitem__(self, key: int) -> tuple[str, T]:
        return self._labels.get(index, index), self._groups.get(index)

    def labels(self) -> list[str]:
        return [self._labels.get(index, index) for index in self._groups]
