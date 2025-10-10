from controllers.ui_controller import ConstructionModeController
from models.event import CLICK_TYPE, Event
from config.settings import PLATFORM_LENGTH
from ui.popups import alert
from services.construction.platform_target import find_platform_target
from graphics.camera import Camera
from domain.rail_map import RailMap
from models.construction import ConstructionState
import pygame
from views.construction.platform import PlatformView

class PlatformController(ConstructionModeController):
    def __init__(self, map: RailMap, state: ConstructionState, camera: Camera, screen: pygame.Surface):
        view = PlatformView(map, state, camera, screen)
        super().__init__(view, map, state, camera)
        
        
    def handle_event(self, event: Event):
        if event.click_type == CLICK_TYPE.RIGHT_CLICK:
            if self._construction_state.platform_state == "select_station":
                self._construction_state.platform_state = None
                return True
            return False

        # if user is currently selecting a station for the platform
        if self._construction_state.platform_state == 'select_station':
            for station_pos in self._map.station_positions:
                if event.world_pos.is_within_station_rect(station_pos):
                    self._map.add_platform_on(
                        self._map.get_station_at(station_pos),
                        list(self._construction_state.preview_edges)
                    )
                    break
            self._construction_state.platform_state = None
            return True

        # otherwise, find target under cursor
        target = find_platform_target(self._map, event.world_pos, self._camera.scale)

        if target.kind in ('none', 'existing_platform'):
            return True  # consumed, nothing to do

        if not target.is_valid:
            alert(f'Platform too short! Minimum length is {PLATFORM_LENGTH} segments.')
            return True

        # prepare to select station
        self._construction_state.platform_state = 'select_station'
        self._construction_state.preview_edges_type = 'platform_selected'
        return True
