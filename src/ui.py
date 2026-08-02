"Management of the screen, keyboard events, timing, and random data."

import time
import random
from constants import *
from blessed import Terminal
from result import Ok, Err, Result
from models import Action, Direction, GameState, History, Position, Snake, Status
from core import pause_game, quit_game, restart_game, start_game, tick, turn_snake

def generate_food(snake: Snake, num_rows: int, num_cols: int) -> Result[Position, str]:
    occupied_spaces = set(snake.body)
    free_spaces = [
        Position(row, col) for row in range(num_rows) for col in range(num_cols) if Position(row, col) not in occupied_spaces
    ]
    return Ok(random.choice(free_spaces)) if free_spaces else Err("No free spaces left on the board.")

def key_to_direction(key: str) -> Result[Direction, str]:
    key = key.lower()
    return Ok(DIRECTION_KEYS[key]) if key in DIRECTION_KEYS else Err("Not a directional key")

def key_to_action(key: str, current_status: Status) -> Result[Action, str]:
    if current_status == Status.QUIT:
            return Err("Quit")
    key = key.lower()
    transitions = ACTION_KEYS.get(current_status, {})
    return Ok(transitions.get(key, transitions.get("_", Action.NONE)))

def handle_control_key(state: GameState, key: str, initial_snake: Snake, initial_food: Position, initial_speed: float) -> GameState:
    match key_to_action(key, state.status):
        case Ok(Action.NONE):
            return state
        case Ok(Action.START):
            return start_game(state)
        case Ok(Action.PAUSE):
            return pause_game(state)
        case Ok(Action.RESUME):
            return start_game(state)
        case Ok(Action.RESTART):
            return restart_game(state, initial_snake, initial_food, initial_speed)
        case Ok(Action.QUIT):
            return quit_game(state)
        case Err(_):
            return state

def get_board_dimensions(terminal: Terminal) -> tuple[int, int]:
    board_rows = terminal.height * (1 - 2 * MARGIN_PERC)
    board_cols = terminal.width * (1 - 2 * MARGIN_PERC)
    return int(board_rows), int(board_cols)

def get_margins(terminal: Terminal) -> tuple[int, int]:
    return int(terminal.height * MARGIN_PERC), int(terminal.width * MARGIN_PERC)

def validate_terminal_dimensions(terminal: Terminal) -> Result[Terminal, str]:
    if terminal.height < MIN_HEIGHT or terminal.width < MIN_WIDTH:
        return Err(
            f"Too small terminal ({terminal.width}x{terminal.height}).\n"
            f"Minimum size: {MIN_WIDTH}x{MIN_HEIGHT}."
        )
    return Ok(terminal)

def draw_board(terminal: Terminal, state: GameState, board_rows: int, board_cols: int) -> str:
    output = []

    horizontal_lines = HORIZONTAL * board_cols
    margin_y, margin_x = get_margins(terminal)
    top_edge = margin_y - 1
    bottom_edge = top_edge + board_rows + 1
    left_edge = margin_x - 1
    right_edge = left_edge + board_cols + 1

    output.append(terminal.move_xy(left_edge, top_edge) + TOP_LEFT + horizontal_lines + TOP_RIGHT)
    output.append(terminal.move_xy(left_edge, bottom_edge) + BOTTOM_LEFT + horizontal_lines + BOTTOM_RIGHT)
    for r in range(board_rows):
        row = margin_y + r
        output.append(terminal.move_xy(left_edge, row) + VERTICAL)
        output.append(terminal.move_xy(right_edge, row) + VERTICAL)

    stats_y = top_edge - 2
    shortcuts_y = bottom_edge + 2

    score_str = f"SCORE: {state.score}"
    record_str = f"BEST: {state.record}"
    speed_str = f"SPEED: {state.speed:.1f}"
    pause_str = "[P] Pause"
    quit_str = "[Q/ESC] Quit"

    GAP = 11
    score_x = left_edge
    pause_x = left_edge
    speed_x = score_x + GAP
    quit_x = pause_x + GAP
    record_x = right_edge + 1 - len(record_str)

    output.append(terminal.move_xy(score_x, stats_y) + terminal.bold_blue(score_str))
    output.append(terminal.move_xy(speed_x, stats_y) + terminal.bold_white(speed_str))
    output.append(terminal.move_xy(record_x, stats_y) + terminal.bold_yellow(record_str))

    output.append(terminal.move_xy(pause_x, shortcuts_y) + terminal.bold_white(pause_str))
    output.append(terminal.move_xy(quit_x, shortcuts_y) + terminal.bold_white(quit_str))

    food_x = margin_x + state.food.col
    food_y = margin_y + state.food.row
    output.append(terminal.move_xy(food_x, food_y) + terminal.red(FOOD))

    head = state.snake.body[0]
    body = state.snake.body[1:]
    
    for segment in body:
        seg_x = margin_x + segment.col
        seg_y = margin_y + segment.row
        output.append(terminal.move_xy(seg_x, seg_y) + terminal.green(BODY))
        
    head_x = margin_x + head.col
    head_y = margin_y + head.row
    output.append(terminal.move_xy(head_x, head_y) + terminal.bold_green(HEAD))
    
    return "".join(output)

def draw_overlay(terminal: Terminal, state: GameState, board_rows: int, board_cols: int) -> str:
    if state.status == Status.RUNNING:
        return ""

    messages = {
        Status.START:   ["WELCOME TO SNAKE".center(OVERLAY_WIDTH, " "), "Press any key".center(OVERLAY_WIDTH, " "), "to start".center(OVERLAY_WIDTH, " ")],
        Status.PAUSED:  ["PAUSED GAME".center(OVERLAY_WIDTH, " "), "[P/ESC] to resume".center(OVERLAY_WIDTH, " "), "[R] to restart".center(OVERLAY_WIDTH, " ")],
        Status.DEFEAT:  ["GAME OVER!".center(OVERLAY_WIDTH, " "), "[R] to try again".center(OVERLAY_WIDTH, " "), "[Q] to quit".center(OVERLAY_WIDTH, " ")],
        Status.VICTORY: ["PERFECT VICTORY!".center(OVERLAY_WIDTH, " "), "[R] to play again".center(OVERLAY_WIDTH, " "), "[Q] to quit".center(OVERLAY_WIDTH, " ")],
    }

    lines = messages.get(state.status, [])
    if not lines:
        return ""
        
    output = []
    margin_y, margin_x = get_margins(terminal)
    start_y = margin_y + (board_rows // 2) - (len(lines) // 2)
    
    for i, line in enumerate(lines):
        start_x = margin_x + max(0, (board_cols // 2) - (len(line) // 2))
        style = terminal.black_on_yellow if state.status == Status.PAUSED else terminal.bold_white_on_red
        output.append(terminal.move_xy(start_x, start_y + i) + style(line))
        
    return "".join(output)

def game_loop(terminal: Terminal) -> Result[list[GameState], str]:
    board_rows, board_cols = get_board_dimensions(terminal)
    initial_snake = Snake(
        body=(Position(board_rows // 2, board_cols // 2),),
        direction=Direction.RIGHT
    )
    initial_food = Position(board_rows // 4, board_cols // 4)
    initial_speed = 5.0
    
    state = GameState(
        status=Status.START,
        snake=initial_snake,
        food=initial_food,
        score=0,
        record=0,
        speed=initial_speed
    )
    
    last_time = time.monotonic()
    accumulator = 0.0
    history: History = []
    
    with terminal.fullscreen(), terminal.cbreak(), terminal.hidden_cursor():
        while state.status != Status.QUIT:
            current_time = time.monotonic()
            delta_time = current_time - last_time
            last_time = current_time
            accumulator += delta_time
            
            board_str = draw_board(terminal, state, board_rows, board_cols)
            overlay_str = draw_overlay(terminal, state, board_rows, board_cols)
            print(terminal.clear + terminal.move_xy(0, 0) + board_str + overlay_str, end="", flush=True)
            
            key = terminal.inkey(timeout=0.016)
            
            if key:
                key_name = str(key.name or key)
                state = handle_control_key(state, key_name, initial_snake, initial_food, initial_speed)
                if state.status == Status.RUNNING:
                    match key_to_direction(key_name):
                        case Ok(new_dir):
                            state = turn_snake(state, new_dir)
                        case Err(_):
                            pass
            
            tick_interval = 1.0 / state.speed if state.speed > 0 else 0.2
            if accumulator >= tick_interval:
                next_food = generate_food(state.snake, board_rows, board_cols).unwrap_or(state.food)
                state = tick(state, next_food, board_rows, board_cols)
                accumulator -= tick_interval
                if state.status == Status.RUNNING:
                    history.append(state)
                    
    return Ok(history)

def run_ui() -> list[GameState]:
    terminal = Terminal()
    return validate_terminal_dimensions(terminal).and_then(game_loop).unwrap_or_else(print)
