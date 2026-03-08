from functools import reduce
from operator import ior

import detroit as d3


class Group:
    __slots__ = "columns", "groups"

    def __init__(self, data, fx, fy):
        match (fx, fy):
            case None, None:
                self.groups = data
                self.columns = []
            case fx, None:
                self.groups = d3.group(data, fx)
                self.columns = [list(self.groups.keys()), None]
            case None, fy:
                self.groups = d3.group(data, fy)
                self.columns = [None, list(self.groups.keys())]
            case fx, fy:
                self.groups = d3.group(data, fx, fy)
                fx_columns = list(self.groups.keys())
                fy_columns = list(
                    reduce(ior, (self.groups[c].keys() for c in fx_columns))  # type: ignore
                )
                self.columns = [fx_columns, fy_columns]
