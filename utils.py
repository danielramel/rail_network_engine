from models import Point
from constants import GRID_SIZE

def get_direction_between_points(p1: Point, p2: Point) -> tuple[int, int]:
    return (signum(p2.x - p1.x), signum(p2.y - p1.y))

def snap_to_grid(x: float, y: float) -> Point:
    snapped_x = round(x / GRID_SIZE) * GRID_SIZE
    snapped_y = round(y / GRID_SIZE) * GRID_SIZE
    return Point(snapped_x, snapped_y)


def signum(x: float) -> int:
    return (x > 0) - (x < 0)

def get_valid_turns(direction: tuple[int, int]) -> list[tuple[int, int]]:
    """Get valid directions we can turn to from the given direction, respecting 45° turn limit."""
    VALID_TURNS = {
        (-1, -1): [(-1, -1), (-1, 0), (0, -1)],
        (-1,  1): [(-1,  1), (-1, 0), (0,  1)],  
        ( 1, -1): [( 1, -1), ( 1, 0), (0, -1)], 
        ( 1,  1): [( 1,  1), ( 1, 0), (0,  1)],
        
        (-1, 0): [(-1, 0), (-1, -1), (-1,  1)],
        ( 1, 0): [( 1, 0), ( 1, -1), ( 1,  1)],
        (0, -1): [(0, -1), (-1, -1), ( 1, -1)],
        (0,  1): [(0,  1), (-1,  1), ( 1,  1)],
        (0,  0): [(-1, -1), (-1, 0), (-1, 1),
                  (1, -1), (1, 0), (1, 1),
                  (0, -1), (0, 1)]
    }
    return VALID_TURNS[direction]