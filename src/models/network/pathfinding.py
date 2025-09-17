from config.settings import GRID_SIZE
from models.geometry import Point, PointWithDirection
import heapq


ORTHOGONAL_COST = 1.0
DIAGONAL_COST = 1.414  # Approximate sqrt(2)

def get_direction_cost(direction: tuple[int, int]) -> float:
    """Get the cost for moving in a given direction."""
    dx, dy = direction
    if dx != 0 and dy != 0:
        return DIAGONAL_COST
    else:
        return ORTHOGONAL_COST

def get_valid_turn_neighbors(state: PointWithDirection) -> list[tuple[PointWithDirection, float]]:
    """
    Get valid neighboring states from current state, respecting 45° turn limit.
    
    Args:
        state: Current state (position + direction)
        
    Returns:
        List of (new_state, cost) tuples
    """
    neighbors = []
    valid_directions = get_valid_turns(state.direction)
    for dx, dy in valid_directions:
        nx = state.point.x + dx * GRID_SIZE
        ny = state.point.y + dy * GRID_SIZE
        new_state = PointWithDirection(Point(nx, ny), (dx, dy))
        cost = get_direction_cost((dx, dy))
        neighbors.append((new_state, cost))
    return neighbors

def heuristic(a: Point, b: Point) -> float:
    """
    Calculate heuristic distance between two points.
    Uses Chebyshev distance for 8-directional movement.
    """
    dx = abs(a.x - b.x) / GRID_SIZE
    dy = abs(a.y - b.y) / GRID_SIZE
    return max(dx, dy)

def reconstruct_path(came_from: dict[PointWithDirection, PointWithDirection], current_state: PointWithDirection) -> tuple[Point, ...]:
    """Reconstruct and simplify the path from states."""
    path = [current_state.point]
    
    while current_state in came_from:
        current_state = came_from[current_state]
        path.append(current_state.point)
    
    # Reverse to get start -> end order, then simplify
    return tuple(reversed(path))

def find_path(start: PointWithDirection, end: Point) -> tuple[Point, ...]:
    """
    Find optimal path using A* algorithm with 45° turn constraint.
    
    Args:
        start: Starting point or state (point + direction). If Point is provided,
                all possible starting directions will be considered.
        end: Target point
        
    Returns:
        Tuple of Point objects representing the path, simplified to direction changes only.
        Empty tuple if no path found.
    """
    # Handle the case where start and end are the same
    if start.point == end:
        return (start.point,)

    # Priority queue: (f_score, current_g, state)
    open_set = []
    came_from: dict[PointWithDirection, PointWithDirection] = {}
    g_score: dict[PointWithDirection, float] = {}
    f_score: dict[PointWithDirection, float] = {}


    g_score[start] = 0
    f_score[start] = heuristic(start.point, end)
    heapq.heappush(open_set, (f_score[start], g_score[start], start))

    while open_set:
        current_f, current_g, current_state = heapq.heappop(open_set)
        
        # Skip if we've already found a better path to this state
        if current_state in g_score and current_g > g_score[current_state]:
            continue
        
        if current_state.point == end:
            return reconstruct_path(came_from, current_state)
        
        for neighbor_state, cost in get_valid_turn_neighbors(current_state):
            tentative_g_score = g_score[current_state] + cost
            
            if neighbor_state not in g_score or tentative_g_score < g_score[neighbor_state]:
                came_from[neighbor_state] = current_state
                g_score[neighbor_state] = tentative_g_score
                f_score[neighbor_state] = tentative_g_score + heuristic(neighbor_state.point, end)
                
                heapq.heappush(open_set, (f_score[neighbor_state], g_score[neighbor_state], neighbor_state))
    
    # No path found
    return ()


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