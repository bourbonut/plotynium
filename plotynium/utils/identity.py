from .maker import Maker

class Identity(Maker):
    def __init__(self):
        pass

    def __call__(self, value):
        return value
