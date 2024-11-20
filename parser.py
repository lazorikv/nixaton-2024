from dataclasses import dataclass
from enum import StrEnum

from models import Input

# Map size is N x N
N = 13


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


@dataclass
class Position:
    i: int
    j: int
    direction: Direction | None


@dataclass
class ParsedData:
    player: Position
    enemies: list[Position]


def is_player_position(cell: str) -> bool:
    return cell.startswith("P")


def is_enemy_position(cell: str) -> bool:
    return cell.startswith("E")


def get_player_direction(cell: str) -> Direction:
    return cell[-1]


def parse_data(input: Input) -> ParsedData:
    player = None
    enemies = []

    matrix = input.field

    for i in range(N):
        for j in range(N):

            cell = matrix[i][j]

            if is_player_position(cell):
                player = Position(i, j, cell[-1])

            elif is_enemy_position(cell):
                enemies.append(Position(i, j, cell[-1]))

    return ParsedData(player, enemies)
