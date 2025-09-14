import pygame
from pathfinding import find_path
from rail_network import RailNetwork
from models import State
from utils import snap_to_grid, get_direction_between_points
from .state import ConstructionState
from .ui_helpers import get_zoom_box, get_construction_buttons

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
                        if mode != state.Mode:
                            state.Mode = mode
                            state.rail_construction_points.clear()
                        return
                zoom_box = get_zoom_box(surface)
                if zoom_box.collidepoint(x, y):
                    camera.reset()
                    state.rail_construction_points.clear()
                    return
                camera.start_drag(x, y)

            elif event.button == 3:
                if state.Mode == ConstructionState.Mode.RAIL and state.rail_construction_points:
                    network.add_segment(
                        network.add_node(state.rail_construction_points[0]).id,
                        network.add_node(state.rail_construction_points[-1]).id,
                        state.rail_construction_points
                    )
                state.rail_construction_points.clear()

        elif event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            if event.button == 1:
                ## previous click was not on a button and no drag happened
                if state.Mode == ConstructionState.Mode.RAIL and camera.is_dragging and x == camera.drag_start_x and y == camera.drag_start_y:
                    snapped = snap_to_grid(*camera.screen_to_world(x, y))
                    if not state.rail_construction_points:
                        state.rail_construction_points.append(snapped)
                    elif snapped != state.rail_construction_points[-1]:
                        if len(state.rail_construction_points) > 1:
                            last_state = State(state.rail_construction_points[-1], get_direction_between_points(state.rail_construction_points[-2], state.rail_construction_points[-1]))
                            found_path = find_path(last_state, snapped)
                        else:
                            found_path = find_path(state.rail_construction_points[0], snapped) # this will consider all directions, so no need to pass direction

                        state.rail_construction_points.extend(found_path)
                camera.stop_drag() # has to say here to avoid issues with button clicks

            
        elif event.type == pygame.MOUSEMOTION:
            if camera.is_dragging:
                camera.update_drag(event.pos[0], event.pos[1])

        elif event.type == pygame.MOUSEWHEEL:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            camera.zoom(mouse_x, mouse_y, event.y, surface.get_width(), surface.get_height())
