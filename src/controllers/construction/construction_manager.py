import pygame
from models.geometry import Position
    
from graphics.camera import Camera
from domain.rail_map import RailMap
from models.construction import ConstructionState, ConstructionMode
from models.event import Event, CLICK_TYPE
from ui.components.base import BaseUIComponent
from ui.components.panel import Panel
from ui.construction.panels.bulldoze_panel import BulldozePanel
from ui.construction.panels.platform_panel import PlatformPanel
from ui.construction.panels.station_panel import StationPanel
from .rail_controller import RailController
from .platform_controller import PlatformController
from .signal_controller import SignalController
from .station_controller import StationController
from .bulldoze_controller import BulldozeController
from views.construction.construction_view import ConstructionCommonView
from .base_construction_controller import BaseConstructionController
from ui.construction.panels.rail_panel import RailPanel
from ui.construction.panels.signal_panel import SignalPanel

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
        self._panels: dict[ConstructionMode, Panel] = {
            ConstructionMode.RAIL: RailPanel(screen, state),
            ConstructionMode.SIGNAL: SignalPanel(screen, state),
            ConstructionMode.STATION: StationPanel(screen, state),
            ConstructionMode.PLATFORM: PlatformPanel(screen, state),
            ConstructionMode.BULLDOZE: BulldozePanel(screen, state)
        }
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in CONSTRUCTION_MODE_KEYS:
                self._construction_state.switch_mode(CONSTRUCTION_MODE_KEYS[event.key])
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._camera.start_drag(event.pos_)

        elif event.type == pygame.MOUSEMOTION:
            self._camera.update_drag(event.pos_)

        elif event.type == pygame.MOUSEWHEEL:
            self._camera.zoom(event.pos_, event.y)

        elif event.type == pygame.MOUSEBUTTONUP:
            was_dragging = self._camera.stop_drag(event.pos_)

            if was_dragging:
                return
            
            if self._construction_state.mode is None:
                return
            
            if event.button not in (1, 3):
                return
            
            click_type = CLICK_TYPE.LEFT_CLICK if event.button == 1 else CLICK_TYPE.RIGHT_CLICK
            event = Event(click_type, event.pos_)
            if self._panels[self._construction_state.mode].handle_event(event):
                return
            self._controllers[self._construction_state.mode].handle_event(event)

            
    def render(self, screen_pos: Position | None):
        self.view.render(screen_pos)
        
        if self._construction_state.mode is None:
            return
        
        if screen_pos is not None:  
            self._controllers[self._construction_state.mode].render(screen_pos)
        self._panels[self._construction_state.mode].render(screen_pos)

    def contains(self, screen_pos: Position) -> bool:
        return True

CONSTRUCTION_MODE_KEYS = {
    pygame.K_1: ConstructionMode.RAIL,
    pygame.K_2: ConstructionMode.SIGNAL,
    pygame.K_3: ConstructionMode.STATION,
    pygame.K_4: ConstructionMode.PLATFORM,
    pygame.K_5: ConstructionMode.BULLDOZE,
}