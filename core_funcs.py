from constants import GRID_SIZE
from rail_network import Point
import heapq
import random

from typing import List, Tuple, Dict





def heuristic(a: Point, b: Point) -> float:
    """
    Calculate heuristic distance between two points.
    Uses Chebyshev distance for 8-directional movement.
    """
    dx = abs(a.x - b.x) / GRID_SIZE
    dy = abs(a.y - b.y) / GRID_SIZE
    return max(dx, dy)


ORTHOGONAL_DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
DIAGONAL_DIRECTIONS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
ORTHOGONAL_COST = 1.0
DIAGONAL_COST = 1.414  # Approximate sqrt(2)

def get_neighbors(point: Point) -> List[Point]:
    """Get all neighboring points and their move costs."""
    neighbors = []
    for dx, dy in ORTHOGONAL_DIRECTIONS:
        nx = point.x + dx * GRID_SIZE
        ny = point.y + dy * GRID_SIZE
        neighbor = Point(nx, ny)
        cost = ORTHOGONAL_COST
        neighbors.append((neighbor, cost))
    for dx, dy in DIAGONAL_DIRECTIONS:
        nx = point.x + dx * GRID_SIZE
        ny = point.y + dy * GRID_SIZE
        neighbor = Point(nx, ny)
        cost = DIAGONAL_COST
        neighbors.append((neighbor, cost))
    return neighbors


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
    
    simplified = [points[0]]  # Always keep first point
    
    # Calculate initial direction vector
    prev_dx = points[1].x - points[0].x
    prev_dy = points[1].y - points[0].y
    
    for i in range(2, len(points)):
        # Calculate current direction vector
        curr_dx = points[i].x - points[i-1].x
        curr_dy = points[i].y - points[i-1].y
        
        # Check if direction changed using cross product
        cross_product = prev_dx * curr_dy - prev_dy * curr_dx
        
        if cross_product != 0:
            # Direction changed, keep the turning point
            simplified.append(points[i-1])
        
        prev_dx, prev_dy = curr_dx, curr_dy
    
    # Always keep last point
    simplified.append(points[-1])
    return tuple(simplified)


def find_path(start: Point, end: Point) -> Tuple[Point, ...]:
    """
    Find optimal path from start to end using A* algorithm.
    
    Args:
        start: Starting point
        end: Target point
        
    Returns:
        Tuple of Point objects representing the path, simplified to direction changes only.
        Empty tuple if no path found.
    """
    if start == end:
        return (start,)
    
    # Priority queue: (f_score, random_tiebreaker, point)
    open_set = []
    heapq.heappush(open_set, (0, random.random(), start))
    
    # Path reconstruction
    came_from: Dict[Point, Point] = {}
    
    # Scores
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}
    
    while open_set:
        current_f, rnd, current = heapq.heappop(open_set)
        
        # Goal reached
        if current == end:
            return _reconstruct_path(came_from, current)
        
        # Explore neighbors
        for neighbor, cost in get_neighbors(current):
            tentative_g_score = g_score[current] + cost

            # If this is a better path to neighbor
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                
                heapq.heappush(open_set, (f_score[neighbor], random.random(), neighbor))
    
    # No path found
    return ()


def _reconstruct_path(came_from: Dict[Point, Point], current: Point) -> Tuple[Point, ...]:
    """Reconstruct and simplify the path."""
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    
    # Reverse to get start -> end order, then simplify
    path.reverse()
    return simplify_path(path)