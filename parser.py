from dataclasses import dataclass
from enum import StrEnum

from models import Input


class CellType(StrEnum):
    PLAYER = "P"
    ENEMY = "E"
    COIN = "C"
    ASTEROID = "A"
    EMPTY = "_"


class Direction(StrEnum):
    NORTH = "N"
    SOUTH = "S"
    WEST = "W"
    EAST = "E"


def parse_data(input: Input):
    ...
