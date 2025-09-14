from models import Point
from constants import GRID_SIZE

ORTHOGONAL_DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
DIAGONAL_DIRECTIONS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

def get_direction_between_points(p1: Point, p2: Point) -> tuple[int, int]:
    dx = p2.x - p1.x
    dy = p2.y - p1.y

    norm_dx = 0 if dx == 0 else (1 if dx > 0 else -1)
    norm_dy = 0 if dy == 0 else (1 if dy > 0 else -1)
    return (norm_dx, norm_dy)

def snap_to_grid(x: float, y: float) -> Point:
    snapped_x = round(x / GRID_SIZE) * GRID_SIZE
    snapped_y = round(y / GRID_SIZE) * GRID_SIZE
    return Point(snapped_x, snapped_y)