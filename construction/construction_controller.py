import pygame
from rail_network import RailNetwork, Point
from .state import ConstructionState
from .ui_helpers import get_zoom_box, get_construction_buttons
from .geometry_utils import snap_to_grid, snap_to_axis

def handle_construction_events(state: ConstructionState, construction_toggle_button, surface, camera, network: RailNetwork):
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            return "quit"

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if event.button == 1:
                if construction_toggle_button.collidepoint(x, y):
                    return "toggle"
                for mode, rect in get_construction_buttons(surface):
                    if rect.collidepoint(x, y):
                        if mode != state.selected_mode:
                            state.selected_mode = mode
                            state.rail_construction_points.clear()
                        return
                zoom_box = get_zoom_box(surface)
                if zoom_box.collidepoint(x, y):
                    camera.reset()
                    return
                camera.start_drag(x, y)

            elif event.button == 3:
                if state.selected_mode.name == "RAIL" and state.rail_construction_points:
                    network.add_segment(
                        network.add_node(state.rail_construction_points[0]).id,
                        network.add_node(state.rail_construction_points[-1]).id,
                        state.rail_construction_points
                    )
                state.rail_construction_points.clear()

        elif event.type == pygame.MOUSEBUTTONUP:
            camera.stop_drag()
            x, y = event.pos
            if event.button == 1:
                if x == camera.drag_start_x and y == camera.drag_start_y:
                    world_x, world_y = camera.screen_to_world(x, y)
                    snapped = snap_to_grid(world_x, world_y)
                    if state.selected_mode.name == "RAIL":
                        if not state.rail_construction_points or (
                            snapped.x != state.rail_construction_points[-1].x or snapped.y != state.rail_construction_points[-1].y
                        ):
                            if state.rail_construction_points:
                                snapped = snap_to_axis(state.rail_construction_points[-1], snapped)
                            state.rail_construction_points.append(snapped)

        elif event.type == pygame.MOUSEMOTION:
            if camera.is_dragging:
                camera.update_drag(event.pos[0], event.pos[1])

        elif event.type == pygame.MOUSEWHEEL:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            camera.zoom(mouse_x, mouse_y, event.y, surface.get_width(), surface.get_height())
