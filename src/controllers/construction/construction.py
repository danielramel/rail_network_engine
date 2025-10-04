import pygame
from models.geometry import Position
from ui.construction.panel import Panel
from ui.core.ui_layer import UILayer
from .rail import handle_rail_click
from .signal import handle_signal_click
from .bulldoze import handle_bulldoze_click
from .station import handle_station_click
from .platform import handle_platform_click
from graphics.camera import Camera
from models.map import RailMap
from models.construction import ConstructionState, ConstructionMode
from ui.popups import alert

def handle_construction_events(ui_layer: UILayer, state: ConstructionState, camera: Camera, map: RailMap):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "quit"

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "quit"
            
            if event.key in CONSTRUCTION_MODE_KEYS:
                set_construction_mode(state, map, CONSTRUCTION_MODE_KEYS[event.key], ui_layer)
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = Position(*event.pos)
            if event.button == 1:
                if ui_layer.handle_click(pos):
                    return
                camera.start_drag(pos)
            elif event.button == 3:
                if state.mode is ConstructionMode.RAIL and state.mode_info['construction_anchor'] is not None:
                    state.mode_info['construction_anchor'] = None
                elif state.mode is ConstructionMode.STATION and state.mode_info['moving_station'] is not None:
                    map.add_station_at(state.mode_info['moving_station'].position, state.mode_info['moving_station'].name)
                    state.mode_info['moving_station'] = None
                else:
                    state.mode = None
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = Position(*event.pos)
            if event.button == 1:
                if camera.is_click(pos):
                    world_pos = camera.screen_to_world(pos)
                    if state.mode == ConstructionMode.RAIL:
                        handle_rail_click(map, world_pos, state.mode_info)
                    elif state.mode == ConstructionMode.SIGNAL:
                        handle_signal_click(map, world_pos)
                    elif state.mode == ConstructionMode.BULLDOZE:
                        handle_bulldoze_click(map, world_pos, camera.scale)
                    elif state.mode == ConstructionMode.STATION:
                        handle_station_click(map, world_pos, state.mode_info)
                    elif state.mode == ConstructionMode.PLATFORM:
                        handle_platform_click(map, world_pos, camera.scale)
                camera.stop_drag() # should be after click check
           
        elif event.type == pygame.MOUSEMOTION:
            camera.update_drag(Position(*event.pos))
        elif event.type == pygame.MOUSEWHEEL:
            camera.zoom(Position(*pygame.mouse.get_pos()), event.y)


CONSTRUCTION_MODE_KEYS = {
    pygame.K_1: ConstructionMode.RAIL,
    pygame.K_2: ConstructionMode.SIGNAL,
    pygame.K_3: ConstructionMode.STATION,
    pygame.K_4: ConstructionMode.PLATFORM,
    pygame.K_5: ConstructionMode.BULLDOZE,
}

def set_construction_mode(state: ConstructionState, map: RailMap, mode: ConstructionMode, ui_layer: UILayer):
    """Helper function to set construction mode with proper validation"""   
    if mode == ConstructionMode.PLATFORM and len(map.stations) == 0:
        alert("You need to build a station first!")
        mode = None
        
    state.switch_mode(mode)