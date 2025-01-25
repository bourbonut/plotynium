from .maker import Maker

class Identity(Maker):
    def __init__(self, value):
        self._value = value

    def __call__(self, *args):
        return self._value
