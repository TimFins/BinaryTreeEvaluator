from enum import Enum


class RedBlackTreeColor(Enum):
    """Enum containing the colors of a red-black tree (red and black).
    """
    RED = "RED"
    BLACK = "BLACK"

    def __str__(self):
        return self.value
