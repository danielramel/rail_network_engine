from controllers.construction.base_construction_controller import BaseConstructionController
from services.construction.bulldoze_target import BulldozeTargetType, find_bulldoze_target
from models.event import CLICK_TYPE, Event
from graphics.camera import Camera
from domain.rail_map import RailMap
from models.construction import ConstructionState
import pygame
from views.construction.bulldoze_view import BulldozeView

class BulldozeController(BaseConstructionController):
    def __init__(self, map: RailMap, state: ConstructionState, camera: Camera, screen: pygame.Surface):
        view = BulldozeView(map, state, camera, screen)
        super().__init__(view, map, state, camera)
        
    def handle_event(self, event: Event):
        if event.click_type == CLICK_TYPE.RIGHT_CLICK:
            self._construction_state.switch_mode(None)
            return

        target = find_bulldoze_target(self._map, event.screen_pos, self._camera.scale)
        if target.kind == BulldozeTargetType.SIGNAL:
            self._map.remove_signal_at(target.pos)
            return True
        elif target.kind == BulldozeTargetType.STATION  :
            self._map.remove_station_at(target.pos)
            return True
        elif target.kind == BulldozeTargetType.PLATFORM:
            self._map.remove_platform_at(target.edge)
            return True
        elif target.kind == BulldozeTargetType.SEGMENT:
            self._map.remove_segment_at(target.edge)
            return True
        return False