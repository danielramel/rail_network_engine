from models.geometry import Point
from config.settings import GRID_SIZE, STATION_RECT_SIZE

def get_direction_between_points(p1: Point, p2: Point) -> tuple[int, int]:
    def signum(x: float) -> int:
        return (x > 0) - (x < 0)
    
    return (signum(p2.x - p1.x), signum(p2.y - p1.y))

def snap_to_grid(x: float, y: float) -> Point:
    snapped_x = round(x / GRID_SIZE) * GRID_SIZE
    snapped_y = round(y / GRID_SIZE) * GRID_SIZE
    return Point(snapped_x, snapped_y)

def rects_overlap(pos1: Point, pos2: Point) -> bool:
    w, h = STATION_RECT_SIZE
    w += GRID_SIZE
    h += GRID_SIZE

    return (
        abs(pos1.x - pos2.x) < w  and
        abs(pos1.y - pos2.y) < h
    )
