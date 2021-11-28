from enum import Enum


class Color(Enum):
    RED = 0             # range:  +delta
    YELLOW = 0.17       # range:  +- delta
    GREEN = 0.33        # range:  +-delta
    CYAN = 0.5          # range:  +-delta
    BLUE = 0.66         # range:  +-delta
    MAGENTA = 0.83      # range:  +-delta
    RED_2 = 1           # range:  -delta

    @classmethod
    def det_color(cls, value):
        delta = 0.17 / 2

        if cls.YELLOW.value - delta <= value < cls.YELLOW.value + delta:
            return cls.YELLOW
        elif cls.GREEN.value - delta <= value < cls.GREEN.value + delta:
            return cls.GREEN
        elif cls.CYAN.value - delta <= value < cls.CYAN.value + delta:
            return cls.CYAN
        elif cls.BLUE.value - delta <= value < cls.BLUE.value + delta:
            return cls.BLUE
        elif cls.MAGENTA.value - delta <= value < cls.MAGENTA.value + delta:
            return cls.MAGENTA
        else:
            return cls.RED
