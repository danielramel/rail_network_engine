import pygame
from enum import Enum
from rail_network import Point, RailNetwork

# Global state for construction mode
network = RailNetwork()
start_rail_node = None
GRID_SIZE = 40

# Construction selector enum
class ConstructionMode(Enum):
    RAIL = 0
    NODE = 1
    LIGHT = 2
    PLATFORM = 3

button_size = 50
button_margin = 10
construction_modes = [ConstructionMode.RAIL, ConstructionMode.NODE, ConstructionMode.LIGHT, ConstructionMode.PLATFORM]
mode_labels = {ConstructionMode.RAIL: 'R', ConstructionMode.NODE: 'N', ConstructionMode.LIGHT: 'L', ConstructionMode.PLATFORM: 'P'}
selected_mode = ConstructionMode.RAIL

def get_construction_buttons(surface):
    w, h = surface.get_size()
    buttons = []
    for i, mode in enumerate(construction_modes):
        rect = pygame.Rect(button_margin + i * (button_size + button_margin), h - button_size - button_margin, button_size, button_size)
        buttons.append((mode, rect))
    return buttons

def snap_to_grid(x, y):
    snapped_x = round(x / GRID_SIZE) * GRID_SIZE
    snapped_y = round(y / GRID_SIZE) * GRID_SIZE
    return Point(snapped_x, snapped_y)

def handle_construction_view(construction_toggle_button, surface):
    global selected_mode, start_rail_node
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            return "quit"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if construction_toggle_button.collidepoint(x, y):
                return "toggle"
        
            for mode, rect in get_construction_buttons(surface):
                if rect.collidepoint(x, y):
                    selected_mode = mode
                    if mode == ConstructionMode.RAIL and selected_mode != ConstructionMode.RAIL:
                        start_rail_node = None
                    return
                
            # handle construction actions
            snapped = snap_to_grid(x, y)
            if selected_mode == ConstructionMode.NODE:
                network.add_node(len(network.nodes), snapped)
                return

            if selected_mode == ConstructionMode.RAIL:
                node = network.find_node_at(snapped)
                if node is not None and node != start_rail_node:
                    if start_rail_node is None:
                        start_rail_node = node
                    else:
                        network.add_segment(start_rail_node.id, node.id, [start_rail_node.pos, node.pos])
                        start_rail_node = None
            
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
        pygame.draw.lines(surface, (200,200,0), False, [(p.x, p.y) for p in pts], 5)
        
    # Draw all nodes
    for node in network.nodes.values():
        pygame.draw.circle(surface, (0,200,200), (int(node.pos.x), int(node.pos.y)), 8)
        
    # Draw preview: todo
        
    # Draw construction mode buttons
    font = pygame.font.SysFont(None, 40)
    for mode, rect in get_construction_buttons(surface):
        color = (0,200,0) if selected_mode == mode else (100,100,100)
        pygame.draw.rect(surface, color, rect, border_radius=8)
        label = mode_labels[mode]
        text = font.render(label, True, (255,255,255))
        text_rect = text.get_rect(center=rect.center)
        surface.blit(text, text_rect)