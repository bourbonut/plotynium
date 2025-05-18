from typing import Generic

from ..types import U, V


class LegendPicker(Generic[U, V]):
    """
    Class which tracks labels established by `fill`, `stroke` or `symbol` arguments in
    `Mark`. It also helps to keep in memory the assocation `(label, value)`.

    Parameters
    ----------
    labels : dict[int, str] | None
        Specified labels

    Examples
    --------

    Without specified `labels`:

    >>> picker = LegendPicker()
    >>> picker("blue")
    'blue'
    >>> picker("blue")
    'blue'
    >>> picker("red")
    'red'
    >>> picker("red")
    'red'
    >>> picker.labels()
    ['0', '1']
    >>> picker[0]
    ('0', 'blue')
    >>> picker[1]
    ('1', 'red')

    With `labels` specified:

    >>> picker = LegendPicker(labels={0: "random", 1: "optimized"})
    >>> picker("blue")
    'blue'
    >>> picker("blue")
    'blue'
    >>> picker("red")
    'red'
    >>> picker("red")
    'red'
    >>> picker.labels()
    ["random", "optimized"]
    >>> picker[0]
    ('random', 'blue')
    >>> picker[1]
    ('optimized', 'red')
    """

    def __init__(self, labels: dict[int, str] | None = None):
        self._labels: dict[int, str] = labels or {}
        self._indices: dict[U, int] = {}
        self._groups: dict[int, V] = {}

    def __call__(self, value: U, result: V) -> U:
        """
        It keeps in memory the value as label. If the value is not found in memory,
        it makes a new label for this value, based on the current length of already
        stored values.

        Parameters
        ----------
        value : T
            Value extracted of a list of data
        result : V
            Result from a `Transformer`

        Returns
        -------
        U
            Same `result` without any modification
        """
        index = self._indices.setdefault(value, len(self._indices))
        self._labels.setdefault(index, value if value != result else index)
        self._groups[index] = result
        return result

    def __getitem__(self, index: int) -> tuple[str, V]:
        """
        Returns the tuple `(label, value)`

        Parameters
        ----------
        index : int
            Index for finding the label and its value

        Returns
        -------
        tuple[str, V]
            `(label, value)`
        """
        return (self._labels.get(index, str(index)), self._groups.get(index))

    def labels(self) -> list[str]:
        """
        Returns the list of labels

        Returns
        -------
        list[str]
            List of labels
        """
        return [self._labels.get(index, str(index)) for index in self._groups]

    def get_mapping(self) -> list[tuple[str, V]]:
        """
        Returns a ordered dictionary of (label, value)

        Returns
        -------
        list[tuple[str, V]]
            List of pairs (labels, colors)
        """
        if self._groups == {0: "none"}:
            return []
        return [self[index] for index in self._groups]
