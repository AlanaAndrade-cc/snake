"Immutable data type definitions."

from enum import Enum, auto
from dataclasses import dataclass

class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

class Status(Enum):
    START = auto()      # initial screen                    press q to QUIT, any other key to RUNNING
    RUNNING = auto()    # game functioning                  press q to QUIT, r to RUNNING, p to PAUSED arrows to change direction
    PAUSED = auto()     # screen with pause message         press q to QUIT, r to RUNNING, esc to RUNNING
    DEFEAT = auto()     # screen with game over message     press q to QUIT, r to RUNNING
    VICTORY = auto()    # screen with victory message       press q to QUIT, r to RUNNING
    QUIT = auto()       # final screen

@dataclass(frozen=True)
class Position:
    row: int
    col: int

type Body = tuple[Position, ...]

@dataclass(frozen=True)
class Snake:
    body: Body
    direction: Direction

@dataclass(frozen=True)
class GameState:
    status: Status
    snake: Snake
    food: Position
    score: int
    record: int
    speed: float