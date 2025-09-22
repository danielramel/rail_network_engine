from models.geometry import Point
from config.settings import BULLDOZE_SENSITIVITY, GRID_SIZE, STATION_RECT_SIZE
from math import hypot

def get_direction_between_points(p1: Point, p2: Point) -> tuple[int, int]:
    def signum(x: float) -> int:
        return (x > 0) - (x < 0)
    
    return (signum(p2.x - p1.x), signum(p2.y - p1.y))

def snap_to_grid(x: float, y: float) -> Point:
    snapped_x = round(x / GRID_SIZE) * GRID_SIZE
    snapped_y = round(y / GRID_SIZE) * GRID_SIZE
    return Point(snapped_x, snapped_y)

def is_point_near_grid(x: float, y: float, camera_scale) -> bool:
    mod_x = x % GRID_SIZE
    mod_y = y % GRID_SIZE

    sensitivity = BULLDOZE_SENSITIVITY * 1.2 / camera_scale**0.7

    return (mod_x < sensitivity or mod_x > GRID_SIZE - sensitivity) and (mod_y < sensitivity or mod_y > GRID_SIZE - sensitivity)


def station_rects_overlap(pos1: Point, pos2: Point) -> bool:
    w, h = STATION_RECT_SIZE
    w += GRID_SIZE
    h += GRID_SIZE

    return (
        abs(pos1.x - pos2.x) < w  and
        abs(pos1.y - pos2.y) < h
    )

def point_within_station_rect(point: Point, center: Point) -> bool:
    w, h = STATION_RECT_SIZE
    w += GRID_SIZE
    h += GRID_SIZE

    return (
        abs(center.x - point.x) * 2 < w and
        abs(center.y - point.y) * 2 < h
    )
    


def point_line_intersection(p: Point, a: Point, b: Point, camera_scale) -> bool:
    """
    Check if point p is within 'BULLDOZE_SENSITIVITY' pixels of line segment ab.
    """
    # Line vector
    dx, dy = b.x - a.x, b.y - a.y

    t = ((p.x - a.x) * dx + (p.y - a.y) * dy) / (dx*dx + dy*dy)
    t = max(0, min(1, t))  # clamp to segment

    # Closest point on the segment
    cx, cy = a.x + t * dx, a.y + t * dy

    # Distance from p to that closest point
    dist = hypot(p.x - cx, p.y - cy)

    return dist <= BULLDOZE_SENSITIVITY / camera_scale
