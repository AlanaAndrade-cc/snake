"Declarative functions that manipulate game states."

from dataclasses import replace
from result import Ok, Err, Result
from models import Direction, GameState, Position, Snake, Status

INVALID_DIRECTION_TRANSITIONS = {
    frozenset((Direction.UP, Direction.DOWN)),
    frozenset((Direction.LEFT, Direction.RIGHT)),
}

def validate_direction_transition(current: Direction, new: Direction) -> Direction:
    return current if frozenset((current, new)) in INVALID_DIRECTION_TRANSITIONS else new

def turn(snake: Snake, new_direction: Direction) -> Snake:
    return replace(snake, direction=validate_direction_transition(snake.direction, new_direction))

def next_head(snake: Snake, board_rows: int, board_cols: int) -> Position:
    head = snake.body[0]
    direction = snake.direction
    match direction:
        case Direction.RIGHT: row_inc, col_inc = (0, 1)
        case Direction.LEFT: row_inc, col_inc = (0, -1)
        case Direction.UP: row_inc, col_inc = (-1, 0)
        case Direction.DOWN: row_inc, col_inc = (1, 0)
        case _: row_inc, col_inc = (0, 0)
    return Position(
        (head.row + row_inc) % board_rows, (head.col + col_inc) % board_cols
    )

def slide(snake: Snake, board_rows: int, board_cols: int) -> Snake:
    new_head = next_head(snake, board_rows, board_cols)
    new_body = (new_head,) + snake.body
    return replace(snake, body=new_body)

def lose_tail(snake: Snake) -> Snake:
    return replace(snake, body=snake.body[:-1])

def is_eating(snake: Snake, food: Position) -> bool:
    return snake.body[0] == food

def is_colliding(snake: Snake) -> bool:
    head, body = snake.body[0], snake.body[1:]
    return head in body

def run_game(state: GameState, next_food: Position, board_rows: int, board_cols: int) -> GameState:
    new_snake = slide(state.snake, board_rows, board_cols)
    ate = is_eating(new_snake, state.food)

    if not ate: new_snake = lose_tail(new_snake)
    if is_colliding(new_snake): return replace(state, status=Status.DEFEAT)
    if ate and len(new_snake.body) == board_rows * board_cols:
        new_score = state.score + 1
        return replace(
            state,
            status=Status.VICTORY,
            snake=new_snake,
            score=new_score,
            record=max(new_score, state.record)
        )

    new_score = state.score + (1 if ate else 0)
    new_food = next_food if ate else state.food
    new_speed = state.speed * 1.05 if ate else state.speed

    return replace(
        state,
        status=Status.RUNNING,
        snake=new_snake,
        food=new_food,
        score=new_score,
        record=max(new_score, state.record),
        speed=new_speed
    )

def pause_game(state: GameState) -> GameState:
    return replace(state, status=Status.PAUSED)

def restart_game(state: GameState, initial_snake: Snake, initial_food: Position, initial_speed: float) -> GameState:
    return replace(
        state, 
        status=Status.START, 
        snake=initial_snake, 
        food=initial_food,
        score=0, 
        record=max(state.score, state.record), 
        speed=initial_speed
    )

def quit_game(state: GameState) -> GameState:
    return replace(state, status=Status.QUIT)

def tick(state: GameState, next_food: Position, board_rows: int, board_cols: int) -> GameState:
    if state.status == Status.RUNNING:
        return run_game(state, next_food, board_rows, board_cols)
    return state
