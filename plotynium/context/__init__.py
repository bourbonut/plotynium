from .channel import Channel
from ..schemes import Scheme
from ..interpolations import Interpolation
from typing import TypeVar
from detroit.types import Scaler

__all__ = ["Context", "MarkContext"]

TContext = TypeVar("Context", bound="Context")

class MarkContext:

    def __init__(
        self,
        index: int,
        x: int,
        y: int,
        width: int,
        height: int,
        context: TContext,
    ):
        self._index = index
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._context = context

    def half_width(self):
        return self._width // 2

    def half_height(self):
        return self._height // 2

    def vertical_split(self, width: int, opposite: bool = False):
        if width > self._width:
            raise ValueError(
                f"Width(={width}) must be inferior to the width of the group "
                f"context(={self._width})"
            )
        remain = self._width - width
        if opposite:
            self._context.append_group(self._x, self._y, width, self._height)
            self._x += width
            self._width = remain
        else:
            self._context.append_group(self._x + width, self._y, remain, self._height)
            self._width = width

    def horizontal_split(self, height: int, opposite: bool = False):
        if height > self._height:
            raise ValueError(
                f"Height(={height}) must be inferior to the height of the group "
                f"context(={self._height})"
            )
        remain = self._height - height
        if opposite:
            self._context.append_group(self._x, self._y, self._width, height)
            self._y += height
            self._height = remain
        else:
            self._context.append_group(self._x, self._y + height, self._width, remain)
            self._height = height

    @property
    def x(self):
        return self._context._x

    @property
    def y(self):
        return self._context._y

    def __str__(self):
        return (
            f"MarkContext(index={self._index}, x={self._x}, y={self._y},"
            f" width={self._width}, height={self._height})"
        )

    def __repr__(self):
        return str(self)

class Context:

    def __init__(
        self,
        x: Scaler,
        y: Scaler,
        width: int,
        height: int,
        margin_top: int,
        margin_left: int,
        margin_bottom: int,
        margin_right: int,
        color_scheme: Interpolation | Scheme | None = None,
    ):
        """

        Parameters
        ----------
        x : Scaler
            This argument is a scaler for x axis which behaves like a function. By
            passing a data, it returns the x position on the plot.
        y : Scaler
            This argument is a scaler for y axis which behaves like a function. By
            passing a data, it returns the y position on the plot.
        width : int
            
        height : int
            
        margin_top : int
            
        margin_left : int
            
        margin_bottom : int
            
        margin_right : int
            
        color_scheme : Interpolation | Scheme | None
            
        """
        self._x = x
        self._y = y
        self._width = width
        self._height = height 
        self._margin_top = margin_top
        self._margin_left = margin_left 
        self._margin_bottom = margin_bottom 
        self._margin_right = margin_right
        self._channel = Channel()
        self._scheme = None
        self._groups = []

    def get_lu_corner(self) -> tuple[int, int]:
        return (self._margin_left, self._margin_top)

    def get_dims(self) -> tuple[int, int]:
        return (self._width, self._height)

    def get_group_context(self, index: int | None = None):
        if index is not None and 0 <= index < len(self._groups):
            return self._groups[index]
        else:
            x, y = self.get_lu_corner()
            w, h = self.get_dims()
            dx, dy = self.get_lu_corner()
            group_context = MarkContext(len(self._groups), x, y, w - dx, h - dy, self)
            self._groups.append(group_context)
            return group_context

    def append_group(self, x: int, y: int, width: int, height: int):
        group_context = MarkContext(len(self._groups), x, y, width, height, self)
        self._groups.append(group_context)
        return group_context

    def set_channel(self, channels: list[Channel]):
        pass
