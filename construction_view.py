
import pygame
from rail_network import Point, RailNetwork

# Global state for construction mode
network = RailNetwork()
dragging = False
drag_start = None
drag_end = None
GRID_SIZE = 40  # pixels

def snap_to_grid(x, y):
    return (round(x / GRID_SIZE) * GRID_SIZE, round(y / GRID_SIZE) * GRID_SIZE)

def restrict_direction(start, end):
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
    if dx == 0:
        # Vertical
        return (x1, y2)
    if dy == 0:
        # Horizontal
        return (x2, y1)
    # Diagonal: force to closest 45-degree
    if abs(dx) > abs(dy):
        sign = 1 if dy >= 0 else -1
        return (x2, y1 + sign * abs(dx))
    else:
        sign = 1 if dx >= 0 else -1
        return (x1 + sign * abs(dy), y2)

def handle_construction_view(construction_toggle_button):
    global dragging, drag_start, drag_end
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            return "quit"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if construction_toggle_button.collidepoint(x, y):
                return "toggle"
            # Start rail creation
            dragging = True
            drag_start = snap_to_grid(x, y)
            drag_end = drag_start
        elif event.type == pygame.MOUSEMOTION and dragging:
            x, y = event.pos
            snapped = snap_to_grid(x, y)
            drag_end = restrict_direction(drag_start, snapped)
        elif event.type == pygame.MOUSEBUTTONUP and dragging:
            # Finish rail creation
            dragging = False
            x1, y1 = drag_start
            x2, y2 = drag_end
            # Prevent zero-length rails
            if (x1, y1) != (x2, y2):
                node1 = network.add_node(len(network.nodes), Point(x1, y1))
                node2 = network.add_node(len(network.nodes), Point(x2, y2))
                network.add_segment(node1.id, node2.id, [Point(x1, y1), Point(x2, y2)])
            drag_start = None
            drag_end = None
    return None
            
def render_construction_view(surface):
    # Draw grid
    w, h = surface.get_size()
    for gx in range(0, w, GRID_SIZE):
        pygame.draw.line(surface, (60,60,60), (gx, 0), (gx, h))
    for gy in range(0, h, GRID_SIZE):
        pygame.draw.line(surface, (60,60,60), (0, gy), (w, gy))
    # Draw all rails
    for segment in network.segments:
        pts = segment.points
        if len(pts) >= 2:
            pygame.draw.lines(surface, (200,200,0), False, [(p.x, p.y) for p in pts], 5)
    # Draw all nodes
    for node in network.nodes.values():
        pygame.draw.circle(surface, (0,200,200), (int(node.pos.x), int(node.pos.y)), 8)
    # Draw preview if dragging
    if dragging and drag_start and drag_end:
        pygame.draw.line(surface, (255,0,0), drag_start, drag_end, 3)