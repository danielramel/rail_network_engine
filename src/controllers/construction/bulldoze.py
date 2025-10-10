from controllers.ui_controller import ConstructionModeController
from services.construction.bulldoze_target import find_bulldoze_target
from models.event import CLICK_TYPE, Event
from graphics.camera import Camera
from domain.rail_map import RailMap
from models.construction import ConstructionState
import pygame
from views.construction.bulldoze import BulldozeView

class BulldozeController(ConstructionModeController):
    def __init__(self, map: RailMap, state: ConstructionState, camera: Camera, screen: pygame.Surface):
        view = BulldozeView(map, state, camera, screen)
        super().__init__(view, map, state, camera)
        
    def handle_event(self, event: Event):
        if event.click_type != CLICK_TYPE.LEFT_CLICK:
            return False

        target = find_bulldoze_target(self._map, event.world_pos, self._camera.scale)
        if target.kind == 'signal':
            self._map.remove_signal_at(target.pos)
            return True
        elif target.kind == 'station':
            self._map.remove_station_at(target.pos)
            return True
        elif target.kind == 'platform':
            self._map.remove_platform_at(target.edge)
            return True
        elif target.kind == 'segment':
            self._map.remove_segment_at(target.edge)
            return True
        return False