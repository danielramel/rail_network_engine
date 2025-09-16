import pygame
from graphics.camera import Camera
from construction.modes import handle_rail_click, handle_signal_click, handle_bulldoze_click
from network import RailNetwork
from .models import ConstructionState
from .ui_helpers import get_zoom_box, get_construction_buttons

def handle_construction_events(state: ConstructionState, construction_toggle_button, surface, camera: Camera, network: RailNetwork):
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
                    if state.Mode == ConstructionState.Mode.RAIL:
                        handle_rail_click(state, camera, network, event.pos)
                    elif state.Mode == ConstructionState.Mode.SIGNAL:
                        handle_signal_click(state, camera, network, event.pos)
                    elif state.Mode == ConstructionState.Mode.BULLDOZE:
                        handle_bulldoze_click(state, camera, network, event.pos)
                    
                
                camera.stop_drag() # should be after click check
            
        elif event.type == pygame.MOUSEMOTION:
            camera.update_drag(event.pos[0], event.pos[1])

        elif event.type == pygame.MOUSEWHEEL:
            camera.zoom(pygame.mouse.get_pos(), event.y, surface)
