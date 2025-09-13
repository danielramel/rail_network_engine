import pygame
from enum import Enum
from rail_network import Point

start_rail_node = None
mouse_down_pos = None
mouse_dragged = False
GRID_SIZE = 40

# Construction selector enum
class ConstructionMode(Enum):
    RAIL = 'R'
    NODE = 'N'
    LIGHT = 'L'
    PLATFORM = 'P'

selected_mode = ConstructionMode.RAIL

def get_zoom_box(surface):
    return pygame.Rect(surface.get_width() - 100, 10, 80, 30)

def get_construction_buttons(surface):
    button_size = 50
    button_margin = 10
    w, h = surface.get_size()
    buttons = []
    for i, mode in enumerate(ConstructionMode):
        print(mode)
        rect = pygame.Rect(button_margin + i * (button_size + button_margin), h - button_size - button_margin, button_size, button_size)
        buttons.append((mode, rect))
    return buttons

def snap_to_grid(x, y):
    snapped_x = round(x / GRID_SIZE) * GRID_SIZE
    snapped_y = round(y / GRID_SIZE) * GRID_SIZE
    return Point(snapped_x, snapped_y)


def handle_construction_view(construction_toggle_button, surface, camera, network):
    global selected_mode, start_rail_node, mouse_down_pos, mouse_dragged

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            return "quit"

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            mouse_down_pos = (x, y)
            mouse_dragged = False

            if event.button == 1:  # Left click
                if construction_toggle_button.collidepoint(x, y):
                    return "toggle"

                # Check construction mode buttons
                for mode, rect in get_construction_buttons(surface):
                    if rect.collidepoint(x, y):
                        if mode != selected_mode:
                            selected_mode = mode
                            start_rail_node = None
                        return

                # Check zoom reset
                zoom_box = get_zoom_box(surface)
                if zoom_box.collidepoint(x, y):
                    camera.reset()
                    return

                # For construction, wait for mouse up to place
                # Start dragging if not clicking a UI element
                camera.start_drag(x, y)

        elif event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            if event.button == 1:  # Left mouse button
                # Only place if no drag
                if x == camera.drag_start_x and y == camera.drag_start_y:
                    world_x, world_y = camera.screen_to_world(x, y)
                    snapped = snap_to_grid(world_x, world_y)
                    if selected_mode == ConstructionMode.NODE:
                        network.add_node(len(network.nodes), snapped)
                    elif selected_mode == ConstructionMode.RAIL:
                        node = network.find_node_at(snapped)
                        if start_rail_node is None:
                            start_rail_node = node
                        else:
                            if node is not None:
                                network.add_segment(start_rail_node.id, node.id, [start_rail_node.pos, node.pos])
                            start_rail_node = None
                camera.stop_drag()

        elif event.type == pygame.MOUSEMOTION:
            if camera.is_dragging:
                camera.update_drag(event.pos[0], event.pos[1])

        elif event.type == pygame.MOUSEWHEEL:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            camera.zoom(mouse_x, mouse_y, event.y, surface.get_width(), surface.get_height())

def draw_grid(surface, camera):
    """Draw grid lines with camera transform"""
    w, h = surface.get_size()
    
    # Calculate world bounds visible on screen
    world_left, world_top = camera.screen_to_world(0, 0)
    world_right, world_bottom = camera.screen_to_world(w, h)
    
    # Calculate grid line positions
    start_x = int(world_left // GRID_SIZE) * GRID_SIZE
    start_y = int(world_top // GRID_SIZE) * GRID_SIZE
    
    # Draw vertical grid lines
    x = start_x
    while x <= world_right + GRID_SIZE:
        screen_x, _ = camera.world_to_screen(x, 0)
        if 0 <= screen_x <= w:
            pygame.draw.line(surface, (60, 60, 60), (screen_x, 0), (screen_x, h))
        x += GRID_SIZE
    
    # Draw horizontal grid lines
    y = start_y
    while y <= world_bottom + GRID_SIZE:
        _, screen_y = camera.world_to_screen(0, y)
        if 0 <= screen_y <= h:
            pygame.draw.line(surface, (60, 60, 60), (0, screen_y), (w, screen_y))
        y += GRID_SIZE

def render_construction_view(surface, camera, network):
    # Draw grid
    draw_grid(surface, camera)

    # Draw all rails
    for segment in network.segments:
        pts = segment.points
        screen_points = []
        for p in pts:
            screen_x, screen_y = camera.world_to_screen(p.x, p.y)
            screen_points.append((screen_x, screen_y))
        
        if len(screen_points) >= 2:
            pygame.draw.lines(surface, (200, 200, 0), False, screen_points, max(1, int(5 * camera.scale)))
    
    # Draw all nodes
    for node in network.nodes.values():
        screen_x, screen_y = camera.world_to_screen(node.pos.x, node.pos.y)
        radius = max(3, int(8 * camera.scale))
        pygame.draw.circle(surface, (0, 200, 200), (int(screen_x), int(screen_y)), radius)
    
    # Draw rail construction preview
    if selected_mode == ConstructionMode.RAIL and start_rail_node is not None:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        world_x, world_y = camera.screen_to_world(mouse_x, mouse_y)
        snapped = snap_to_grid(world_x, world_y)
        
        start_screen_x, start_screen_y = camera.world_to_screen(start_rail_node.pos.x, start_rail_node.pos.y)
        end_screen_x, end_screen_y = camera.world_to_screen(snapped.x, snapped.y)
        
        pygame.draw.line(surface, (100, 100, 0), 
                        (start_screen_x, start_screen_y), 
                        (end_screen_x, end_screen_y), 
                        max(1, int(3 * camera.scale)))
    
    # Draw construction mode buttons
    font = pygame.font.SysFont(None, 40)
    for mode, rect in get_construction_buttons(surface):
        color = (0, 200, 0) if selected_mode == mode else (100, 100, 100)
        pygame.draw.rect(surface, color, rect, border_radius=8)
        label = mode.value
        text = font.render(label, True, (255, 255, 255))
        text_rect = text.get_rect(center=rect.center)
        surface.blit(text, text_rect)
    
    # Draw zoom indicator
    if camera.scale != 1.0 or camera.x != 0 or camera.y != 0:
        zoom_text = f"{int(camera.scale * 100)}%"
        zoom_font = pygame.font.SysFont(None, 24)
        zoom_surface = zoom_font.render(zoom_text, True, (255, 255, 255))
        zoom_box = get_zoom_box(surface)
        pygame.draw.rect(surface, (50, 50, 50), zoom_box, border_radius=4)
        pygame.draw.rect(surface, (150, 150, 150), zoom_box, 2, border_radius=4)
        text_rect = zoom_surface.get_rect(center=zoom_box.center)
        surface.blit(zoom_surface, text_rect)