import pygame
from models.geometry import Position
    
from graphics.camera import Camera
from domain.rail_map import RailMap
from models.construction import ConstructionState, ConstructionMode
from models.event import Event, CLICK_TYPE
from ui.components.base import BaseUIComponent
from .rail_controller import RailController
from .platform_controller import PlatformController
from .signal_controller import SignalController
from .station_controller import StationController
from .bulldoze_controller import BulldozeController
from views.construction.construction_view import ConstructionCommonView
from .base_construction_controller import BaseConstructionController
from ui.construction.panels.rail_panel import RailPanel

class ConstructionManager(BaseUIComponent):
    def __init__(self, map: RailMap, state: ConstructionState, camera: Camera, screen: pygame.Surface):
        self.view = ConstructionCommonView(map, state, camera, screen)
        self._map = map
        self._construction_state = state
        self._camera = camera

        self._controllers: dict[ConstructionMode, BaseConstructionController] = {
            ConstructionMode.RAIL: RailController(map, state, camera, screen),
            ConstructionMode.SIGNAL: SignalController(map, state, camera, screen),
            ConstructionMode.STATION: StationController(map, state, camera, screen),
            ConstructionMode.PLATFORM: PlatformController(map, state, camera, screen),
            ConstructionMode.BULLDOZE: BulldozeController(map, state, camera, screen),
        }
        self._panels = {
            ConstructionMode.RAIL: RailPanel(screen, state)
        }
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in CONSTRUCTION_MODE_KEYS:
                self._construction_state.switch_mode(CONSTRUCTION_MODE_KEYS[event.key])
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._camera.start_drag(Position(*event.pos))

        elif event.type == pygame.MOUSEMOTION:
            self._camera.update_drag(Position(*event.pos))
            
        elif event.type == pygame.MOUSEWHEEL:
            self._camera.zoom(Position(*pygame.mouse.get_pos()), event.y)
            
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = Position(*event.pos)
            was_dragging = self._camera.stop_drag()
            
            if not was_dragging:
                return
            
            if self._construction_state.mode is None:
                return
            
            click_type = CLICK_TYPE.LEFT_CLICK if event.button == 1 else CLICK_TYPE.RIGHT_CLICK
            event = Event(click_type, pos)
            if self._panels[self._construction_state.mode].handle_event(event):
                return
            self._controllers[self._construction_state.mode].handle_event(event)

            
    def render(self):
        self.view.render()
        if self._construction_state.mode is None:
            return
        
        world_pos = self._camera.screen_to_world(Position(*pygame.mouse.get_pos()))
        if self._construction_state.mode is None:
            return
        
        self._controllers[self._construction_state.mode].render(world_pos)
        self._panels[self._construction_state.mode].render(world_pos)


CONSTRUCTION_MODE_KEYS = {
    pygame.K_1: ConstructionMode.RAIL,
    pygame.K_2: ConstructionMode.SIGNAL,
    pygame.K_3: ConstructionMode.STATION,
    pygame.K_4: ConstructionMode.PLATFORM,
    pygame.K_5: ConstructionMode.BULLDOZE,
}