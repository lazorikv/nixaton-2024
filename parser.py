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
    type: CellType
    direction: Direction | None = None


@dataclass
class Matrix:
    cells: list[Position]

@dataclass
class ParsedData:
    player: Position
    enemies: list[Position]
    matrix: Matrix


def is_player_position(cell: str) -> bool:
    return cell.startswith(CellType.PLAYER)


def is_enemy_position(cell: str) -> bool:
    return cell.startswith(CellType.ENEMY)


def is_asteroid_position(cell: str) -> bool:
    return cell == CellType.ASTEROID


def is_coin_position(cell: str) -> bool:
    return cell == CellType.COIN


def is_empty_position(cell: str) -> bool:
    return cell == CellType.EMPTY


def get_player_direction(cell: str) -> Direction:
    # cause of the bug with ENORTH instead of the EN, etc
    return cell[1]


def parse_data(input: Input) -> ParsedData:
    cells = []
    player = None
    enemies = []

    matrix = input.field

    for i in range(N):
        for j in range(N):

            cell = matrix[i][j]

            if is_player_position(cell):
                player = Position(i, j, CellType.PLAYER, get_player_direction(cell),)
                cells.append(player)

            elif is_enemy_position(cell):
                enemy = Position(i, j, CellType.ENEMY, get_player_direction(cell))
                enemies.append(enemy)
                cells.append(enemy)
            
            else:
                cells.append(Position(i, j, type=cell))

    return ParsedData(player, enemies, Matrix(cells))
