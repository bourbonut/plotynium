from .transformer import Transformer
from ..types import U, V
from .picker import LegendPicker
from collections import OrderedDict

class Default(Transformer[U, V]):

    def __init__(self, data: list[U], value: Callable[[U], V]):
        self._transform = value
        self._picker = LegendPicker()
        
    def __call__(self, d: U) -> V:
        return self._picker(d, self._transform(d))

    def labels(self) -> list:
        return self._picker.labels()

    def __getitem__(self, d: U) -> V:
        return self._picker[d]
