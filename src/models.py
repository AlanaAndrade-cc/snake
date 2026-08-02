"Immutable data type definitions."

from enum import Enum, auto
from dataclasses import dataclass

class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

class Status(Enum):
    START = auto()
    RUNNING = auto()
    PAUSED = auto()
    DEFEAT = auto()
    VICTORY = auto()
    QUIT = auto()

class Action(Enum):
    NONE = auto()
    START = auto()
    PAUSE = auto()
    RESUME = auto()
    RESTART = auto()
    QUIT = auto()

@dataclass(frozen=True)
class Position:
    row: int
    col: int

Body = tuple[Position, ...]

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

History = list[GameState]