from models import Action, Direction, Status

MIN_HEIGHT = 20
MIN_WIDTH = 40
MARGIN_PERC = 0.1
OVERLAY_WIDTH = 30

TOP_LEFT = "┌"
TOP_RIGHT = "┐"
BOTTOM_LEFT = "└"
BOTTOM_RIGHT = "┘"
HORIZONTAL = "─"
VERTICAL = "│"
FOOD = "●"
HEAD = "0"
BODY = "o"

DIRECTION_KEYS = {
    "w": Direction.UP,
    "s": Direction.DOWN,
    "a": Direction.LEFT,
    "d": Direction.RIGHT,
    "key_up": Direction.UP,
    "key_down": Direction.DOWN,
    "key_left": Direction.LEFT,
    "key_right": Direction.RIGHT,
}

ACTION_KEYS = {
    Status.START: {
        "q": Action.QUIT,
        "key_escape": Action.QUIT,
        "_": Action.START,
    },
    Status.RUNNING: {
        "p": Action.PAUSE,
        "q": Action.QUIT,
        "key_escape": Action.QUIT,
        "_": Action.NONE,
    },
    Status.PAUSED: {
        "r": Action.RESTART,
        "p": Action.RESUME,
        "key_escape": Action.RESUME,
        "q": Action.QUIT,
        "_": Action.NONE,
    },
    Status.DEFEAT: {
        "r": Action.RESTART,
        "q": Action.QUIT,
        "key_escape": Action.QUIT,
        "_": Action.NONE,
    },
    Status.VICTORY: {
        "r": Action.RESTART,
        "q": Action.QUIT,
        "key_escape": Action.QUIT,
        "_": Action.NONE,
    },
}