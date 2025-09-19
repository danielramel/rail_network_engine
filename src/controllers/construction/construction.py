import pygame
from ui_elements.construction_buttons import get_zoom_box, get_construction_buttons
from .rail import handle_rail_click
from .signal import handle_signal_click
from .bulldoze import handle_bulldoze_click
from .station import handle_station_click
from graphics.camera import Camera
from models.map import RailMap
from models.construction import ConstructionState

def handle_construction_events(state: ConstructionState, construction_toggle_button, surface, camera: Camera, network: RailMap):
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
                            state.construction_anchor = None
                        return
                if get_zoom_box(surface).collidepoint(x, y):
                    camera.reset()
                    state.construction_anchor = None
                    return
                
                camera.start_drag(x, y)

            elif event.button == 3:
                state.construction_anchor = None

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if camera.is_click(event.pos):
                    pos = camera.screen_to_world(*event.pos)
                    if state.Mode == ConstructionState.Mode.RAIL:
                        handle_rail_click(state, network, pos)
                    elif state.Mode == ConstructionState.Mode.SIGNAL:
                        handle_signal_click(state, network, pos)
                    elif state.Mode == ConstructionState.Mode.BULLDOZE:
                        handle_bulldoze_click(state, network, pos)
                    elif state.Mode == ConstructionState.Mode.STATION:
                        handle_station_click(state, network, pos)

                camera.stop_drag() # should be after click check
            
        elif event.type == pygame.MOUSEMOTION:
            camera.update_drag(event.pos[0], event.pos[1])

        elif event.type == pygame.MOUSEWHEEL:
            camera.zoom(pygame.mouse.get_pos(), event.y, surface)
