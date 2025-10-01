import pygame
from models.geometry import Position
from ui_elements.alert import alert
from ui_elements import get_zoom_box, get_construction_buttons
from .rail import handle_rail_click
from .signal import handle_signal_click
from .bulldoze import handle_bulldoze_click
from .station import handle_station_click
from .platform import handle_platform_click
from graphics.camera import Camera
from models.map import RailMap
from models.construction import ConstructionState, ConstructionMode

def handle_construction_events(state: ConstructionState, construction_toggle_button: pygame.Rect, surface: pygame.Surface, camera: Camera, map: RailMap):
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            return "quit"
        elif event.type == pygame.KEYDOWN:
            # Handle number keys 1-5 for construction modes
            if event.key == pygame.K_1:
                set_construction_mode(state, map, ConstructionMode.RAIL)
            elif event.key == pygame.K_2:
                set_construction_mode(state, map, ConstructionMode.SIGNAL)
            elif event.key == pygame.K_3:
                set_construction_mode(state, map, ConstructionMode.STATION)
            elif event.key == pygame.K_4:
                set_construction_mode(state, map, ConstructionMode.PLATFORM)
            elif event.key == pygame.K_5:
                set_construction_mode(state, map, ConstructionMode.BULLDOZE)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = Position(*event.pos)
            if event.button == 1:
                if construction_toggle_button.collidepoint(*pos):
                    return "toggle"
                for mode, rect in get_construction_buttons(surface):
                    if rect.collidepoint(*pos):
                        if mode != state.Mode:
                            set_construction_mode(state, map, mode)
                        return
                if get_zoom_box(surface).collidepoint(*pos):
                    camera.reset()
                    state.construction_anchor = None
                    return
                camera.start_drag(pos)
            elif event.button == 3:
                if state.Mode is ConstructionMode.RAIL and state.construction_anchor is not None:
                    state.construction_anchor = None
                else:
                    state.Mode = None
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = Position(*event.pos)
            if event.button == 1:
                if camera.is_click(pos):
                    world_pos = camera.screen_to_world(pos)
                    if state.Mode == ConstructionMode.RAIL:
                        handle_rail_click(state, map, world_pos)
                    elif state.Mode == ConstructionMode.SIGNAL:
                        handle_signal_click(map, world_pos)
                    elif state.Mode == ConstructionMode.BULLDOZE:
                        handle_bulldoze_click(map, world_pos, camera.scale)
                    elif state.Mode == ConstructionMode.STATION:
                        handle_station_click(map, world_pos)
                    elif state.Mode == ConstructionMode.PLATFORM:
                        handle_platform_click(map, world_pos, camera.scale)
                camera.stop_drag() # should be after click check
           
        elif event.type == pygame.MOUSEMOTION:
            camera.update_drag(Position(*event.pos))
        elif event.type == pygame.MOUSEWHEEL:
            camera.zoom(Position(*pygame.mouse.get_pos()), event.y)

def set_construction_mode(state: ConstructionState, map: RailMap, mode: ConstructionMode):
    """Helper function to set construction mode with proper validation"""
    if mode != state.Mode:
        if mode == ConstructionMode.RAIL:
            state.construction_anchor = None
        elif mode == ConstructionMode.PLATFORM:
            if len(map.stations) == 0:
                alert("You need to build a station first!")
                state.Mode = None
                return
        state.Mode = mode