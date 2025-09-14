import pygame

def handle_normal_events(construction_toggle_button, surface, camera, network):
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            return "quit"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if event.button == 1:  # Left click
                if construction_toggle_button.collidepoint(x, y):
                    return "toggle"
                else:
                    camera.start_drag(x, y)
            elif event.button in (4, 5):  # Scroll up/down
                zoom_direction = 1 if event.button == 4 else -1
                camera.zoom(x, y, zoom_direction, surface.get_width(), surface.get_height())
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left click release
                camera.stop_drag()
        elif event.type == pygame.MOUSEMOTION:
            if camera.is_dragging:
                x, y = event.pos
                camera.update_drag(x, y)
    return None

def render_normal_view(surface, camera, network):
    # Stub for normal view rendering
    pass