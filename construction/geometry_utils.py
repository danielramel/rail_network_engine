from rail_network import Point
from constants import GRID_SIZE

def snap_to_grid(x, y):
    snapped_x = round(x / GRID_SIZE) * GRID_SIZE
    snapped_y = round(y / GRID_SIZE) * GRID_SIZE
    return Point(snapped_x, snapped_y)

def snap_to_axis(start: Point, end: Point) -> Point:
    """Snap end point to the closest of vertical, horizontal, or 45-degree from start."""
    dx = end.x - start.x
    dy = end.y - start.y
    if dx == 0:
        return Point(start.x, end.y)
    if dy == 0:
        return Point(end.x, start.y)
    # Calculate angles to axes
    angle = abs(dy / dx) if dx != 0 else float('inf')
    # Threshold for snapping (tan(22.5°) ≈ 0.414, tan(67.5°) ≈ 2.414)
    if angle < 0.414:
        # Closer to horizontal
        return Point(end.x, start.y)
    elif angle > 2.414:
        # Closer to vertical
        return Point(start.x, end.y)
    else:
        # Snap to 45-degree
        sign_x = 1 if dx >= 0 else -1
        sign_y = 1 if dy >= 0 else -1
        d = min(abs(dx), abs(dy))
        return Point(start.x + sign_x * d, start.y + sign_y * d)