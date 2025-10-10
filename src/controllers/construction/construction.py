import pygame
from models.geometry import Position
from ui.core.ui_element import UIElement
from graphics.camera import Camera
from domain.rail_map import RailMap
from models.construction import ConstructionState, ConstructionMode
from models.event import Event, CLICK_TYPE
from .rail import RailController
from .platform import PlatformController
from .signal import SignalController
from .station import StationController
from .bulldoze import BulldozeController
from views.construction.construction import ConstructionCommonView

class ConstructionController(UIElement):
    def __init__(self, map: RailMap, state: ConstructionState, camera: Camera, screen: pygame.Surface):
        self._map = map
        self._construction_state = state
        self._camera = camera
        self._controllers = {
            ConstructionMode.RAIL: RailController(map, state, camera, screen),
            ConstructionMode.SIGNAL: SignalController(map, state, camera, screen),
            ConstructionMode.STATION: StationController(map, state, camera, screen),
            ConstructionMode.PLATFORM: PlatformController(map, state, camera, screen),
            ConstructionMode.BULLDOZE: BulldozeController(map, state, camera, screen),
        }
        self.view = ConstructionCommonView(map, state, camera, screen)
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in CONSTRUCTION_MODE_KEYS:
                self._construction_state.switch_mode(CONSTRUCTION_MODE_KEYS[event.key])
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = Position(*event.pos)
            if event.button == 1:
                self._camera.start_drag(pos)
            elif event.button == 3:
                event = Event(CLICK_TYPE.RIGHT_CLICK, self._camera.screen_to_world(pos))
                if self._controllers[self._construction_state.mode].handle_event(event):
                    return
                self._construction_state.switch_mode(None)
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = Position(*event.pos)
            if event.button == 1:
                if self._camera.is_click(pos):
                    event = Event(CLICK_TYPE.LEFT_CLICK, self._camera.screen_to_world(pos))
                    self._controllers[self._construction_state.mode].handle_event(event)
                    
                self._camera.stop_drag()
           
        elif event.type == pygame.MOUSEMOTION:
            self._camera.update_drag(Position(*event.pos))
        elif event.type == pygame.MOUSEWHEEL:
            self._camera.zoom(Position(*pygame.mouse.get_pos()), event.y)
            
            
    def render(self):
        self.view.render()
        if self._construction_state.mode is None:
            return
        
        world_pos = self._camera.screen_to_world(Position(*pygame.mouse.get_pos()))
        self._controllers[self._construction_state.mode].render(world_pos)


CONSTRUCTION_MODE_KEYS = {
    pygame.K_1: ConstructionMode.RAIL,
    pygame.K_2: ConstructionMode.SIGNAL,
    pygame.K_3: ConstructionMode.STATION,
    pygame.K_4: ConstructionMode.PLATFORM,
    pygame.K_5: ConstructionMode.BULLDOZE,
}