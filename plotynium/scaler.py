from enum import Enum, auto

class Scaler(Enum):
    BAND = auto()
    CONTINOUS = auto()
    TIME = auto()

def characterize_scaler(scalers: list):
    scalers = set(scalers)
    if len(scalers) > 1:
        raise RuntimeError(f"Found different scalers {scalers}. Some marks cannot be associated between each other.")
    elif len(scalers) == 0:
        raise ValueError("Cannot identify scaler for marks.")
    return scalers.pop()
