from constants import GRID_SIZE
from rail_network import Point
import heapq
from typing import List, Tuple, Dict
from models import PointWithDirection
from utils import get_direction_between_points

# Movement directions
ORTHOGONAL_DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
DIAGONAL_DIRECTIONS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
ALL_DIRECTIONS = ORTHOGONAL_DIRECTIONS + DIAGONAL_DIRECTIONS

ORTHOGONAL_COST = 1.0
DIAGONAL_COST = 1.414  # Approximate sqrt(2)

# Pre-calculated valid turns for 45° constraint
VALID_TURNS = {
    (-1, -1): [(-1, -1), (-1, 0), (0, -1)],
    (-1,  1): [(-1,  1), (-1, 0), (0,  1)],  
    ( 1, -1): [( 1, -1), ( 1, 0), (0, -1)], 
    ( 1,  1): [( 1,  1), ( 1, 0), (0,  1)],
    
    (-1, 0): [(-1, 0), (-1, -1), (-1,  1)],
    ( 1, 0): [( 1, 0), ( 1, -1), ( 1,  1)],
    (0, -1): [(0, -1), (-1, -1), ( 1, -1)],
    (0,  1): [(0,  1), (-1,  1), ( 1,  1)],
}



def get_direction_cost(direction: Tuple[int, int]) -> float:
    """Get the cost for moving in a given direction."""
    dx, dy = direction
    if dx != 0 and dy != 0:
        return DIAGONAL_COST
    else:
        return ORTHOGONAL_COST

def get_valid_turn_neighbors(state: PointWithDirection) -> List[Tuple[PointWithDirection, float]]:
    """
    Get valid neighboring states from current state, respecting 45° turn limit.
    
    Args:
        state: Current state (position + direction)
        
    Returns:
        List of (new_state, cost) tuples
    """
    neighbors = []
    valid_directions = VALID_TURNS[state.direction]
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

def simplify_path(points: List[Point]) -> Tuple[Point, ...]:
    """
    Simplify path by keeping only direction change points.
    
    Args:
        points: List of Point objects representing the full path
        
    Returns:
        Tuple of Point objects containing only direction changes
    """
    if len(points) < 3:
        return tuple(points)
    
    simplified = [points[0]]
    
    prev_dir = get_direction_between_points(points[0], points[1])
    
    for i in range(2, len(points)):
        curr_dir = get_direction_between_points(points[i-1], points[i])
        
        if curr_dir != prev_dir:
            simplified.append(points[i-1])

        prev_dir = curr_dir

    simplified.append(points[-1])
    return tuple(simplified)

def reconstruct_path(came_from: Dict[PointWithDirection, PointWithDirection], current_state: PointWithDirection) -> Tuple[Point, ...]:
    """Reconstruct and simplify the path from states."""
    path = [current_state.point]
    
    while current_state in came_from:
        current_state = came_from[current_state]
        path.append(current_state.point)
    
    # Reverse to get start -> end order, then simplify
    path.reverse()
    return simplify_path(path)

def find_path(start: PointWithDirection, end: Point) -> Tuple[Point, ...]:
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
    came_from: Dict[PointWithDirection, PointWithDirection] = {}
    g_score: Dict[PointWithDirection, float] = {}
    f_score: Dict[PointWithDirection, float] = {}

    if start.direction == (0, 0):
        initial_states = [PointWithDirection(start.point, direction) for direction in ALL_DIRECTIONS]
    else:
        print(start)
        initial_states = [start]
        
    for initial_state in initial_states:
        g_score[initial_state] = 0
        f_score[initial_state] = heuristic(initial_state.point, end)
        heapq.heappush(open_set, (f_score[initial_state], g_score[initial_state], initial_state))
    
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