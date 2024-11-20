from fastapi import FastAPI
from fastapi.params import Body

from models import Input, Output
from parser import CellType, Direction, Matrix, ParsedData, Position, parse_data

app = FastAPI()
from enum import Enum

class Boundries(str, Enum):
    UP = 'up'
    LEFT = 'left'
    RIGHT = 'right'
    DOWN = 'down'


def get_shrinking_boundaries(matrix: Matrix) -> tuple[int, int, int, int]:
    """
    Dynamically calculates the boundaries of the shrinking map based on asteroid positions.
    Returns a tuple (top, bottom, left, right), where:
        - top: the row index of the topmost row with an asteroid
        - bottom: the row index of the bottommost row with an asteroid
        - left: the column index of the leftmost column with an asteroid
        - right: the column index of the rightmost column with an asteroid
    """
    N=13
    top, bottom, left, right = N, 0, N, 0  # Initialize to the full map size

    for i in range(N):
        for j in range(N):
            # Check if the current cell is an asteroid
            if matrix.cells[i * N + j].type == CellType.ASTEROID:
                # Update top, bottom, left, right boundaries based on asteroid positions
                top = min(top, i)
                bottom = max(bottom, i)
                left = min(left, j)
                right = max(right, j)

    return top, bottom, left, right

def is_asteroid_at_position(i: int, j: int, matrix: Matrix) -> bool:
    """
    Checks if there is an asteroid at the given position (i, j) in the matrix.
    """
    for pos in matrix.cells:
        if pos.i == i and pos.j == j and pos.type == CellType.ASTEROID:
            return True
    return False


def avoid_boundary(player: Position, matrix: Matrix):
    top, bottom, left, right = get_shrinking_boundaries(matrix)
    # Now that we know the shrinking boundaries, decide on actions:
    # Check if the player is near any boundary (top, bottom, left, or right)

    if player.i <= top:  # Player is near the top boundary
        if player.direction == Direction.NORTH:
            return 'D'  # Rotate right to face east
        elif player.direction == Direction.SOUTH:
            return 'A'  # Rotate left to face west
        elif player.direction == Direction.WEST:
            return 'D'  # Rotate right to face north
        elif player.direction == Direction.EAST:
            return 'A'  # Rotate left to face south

    elif player.i >= bottom:  # Player is near the bottom boundary
        if player.direction == Direction.NORTH:
            return 'A'  # Rotate left to face west
        elif player.direction == Direction.SOUTH:
            return 'D'  # Rotate right to face east
        elif player.direction == Direction.WEST:
            return 'A'  # Rotate left to face north
        elif player.direction == Direction.EAST:
            return 'D'  # Rotate right to face south

    elif player.j <= left:  # Player is near the left boundary
        if player.direction == Direction.NORTH:
            return 'D'  # Rotate right to face east
        elif player.direction == Direction.SOUTH:
            return 'A'  # Rotate left to face west
        elif player.direction == Direction.WEST:
            return 'D'  # Rotate right to face south
        elif player.direction == Direction.EAST:
            return 'A'  # Rotate left to face north

    elif player.j >= right:  # Player is near the right boundary
        if player.direction == Direction.NORTH:
            return 'A'  # Rotate left to face west
        elif player.direction == Direction.SOUTH:
            return 'D'  # Rotate right to face east
        elif player.direction == Direction.WEST:
            return 'A'  # Rotate left to face north
        elif player.direction == Direction.EAST:
            return 'D'  # Rotate right to face south

    next_i, next_j = player.i, player.j

    if player.direction == Direction.NORTH:
        next_i -= 1
    elif player.direction == Direction.SOUTH:
        next_i += 1
    elif player.direction == Direction.WEST:
        next_j -= 1
    elif player.direction == Direction.EAST:
        next_j += 1

    # Check if there's an asteroid in the direction the player is facing
    if is_asteroid_at_position(next_i, next_j, matrix):
        # If there's an asteroid, rotate to avoid it
        # Rotate to the right if facing north, south, west, or east
        if player.direction == Direction.NORTH:
            return 'D'  # Rotate right to face east
        elif player.direction == Direction.SOUTH:
            return 'A'  # Rotate left to face west
        elif player.direction == Direction.WEST:
            return 'D'  # Rotate right to face north
        elif player.direction == Direction.EAST:
            return 'A'  # Rotate left to face south

    # 3. If not near a boundary and no asteroid blocking the way, move forward
    return 'M'  # Move f


def move_player(player: Position, matrix: Matrix) -> str:
    # Check if the player needs to avoid the boundary
    move = avoid_boundary(player, matrix)
    return move


# Example usage in the game loop
def game_turn(parsed_data: ParsedData):
    player = parsed_data.player
    matrix = parsed_data.matrix
    
    # Decide the next move
    return move_player(player, matrix)


@app.get("/healthz")
async def root():
    return {"status": "OK"}


@app.post("/move")
async def move(input: Input) -> Output:
    parsed_data = parse_data(input)    
    move = game_turn(parsed_data)

    return Output(move)