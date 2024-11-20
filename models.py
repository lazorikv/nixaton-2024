from dataclasses import dataclass


@dataclass
class Input:
    field: list[list[str]]
    narrowingIn: int
    gameId: int


@dataclass
class Output:
    move: str
