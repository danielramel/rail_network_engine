from controllers.construction.base_construction_controller import BaseConstructionController
from models.event import CLICK_TYPE, Event
from config.settings import PLATFORM_LENGTH
from ui.popups import alert
from services.construction.platform_target import find_platform_target
from graphics.camera import Camera
from domain.rail_map import RailMap
from models.construction import ConstructionState, EdgeType, PlatformState
import pygame
from views.construction.platform_view import PlatformView, PlatformTargetType

class PlatformController(BaseConstructionController):
    def __init__(self, map: RailMap, state: ConstructionState, camera: Camera, screen: pygame.Surface):
        view = PlatformView(map, state, camera, screen)
        super().__init__(view, map, state, camera)
        
        
    def handle_event(self, event: Event):
        if event.click_type == CLICK_TYPE.RIGHT_CLICK:
            if self._construction_state.platform_state == PlatformState.SELECT_STATION:
                self._construction_state.platform_state = None
            else:
                self._construction_state.switch_mode(None)
            return
                
        # if user is currently selecting a station for the platform
        if self._construction_state.platform_state == PlatformState.SELECT_STATION:
            for station_pos in self._map.station_positions:
                if event.screen_pos.is_within_station_rect(station_pos):
                    self._map.add_platform_on(
                        self._map.get_station_at(station_pos),
                        list(self._construction_state.preview_edges)
                    )
                    break
            self._construction_state.platform_state = None
            return

        # otherwise, find target under cursor
        target = find_platform_target(self._map, self._camera.screen_to_world(event.screen_pos), self._camera.scale)

        if target.kind in (PlatformTargetType.NONE, PlatformTargetType.EXISTING_PLATFORM):
            return

        if not target.is_valid:
            alert(f'Platform too short! Minimum length is {PLATFORM_LENGTH} segments.')
            return

        # prepare to select station
        self._construction_state.platform_state = PlatformState.SELECT_STATION
        self._construction_state.preview_edges_type = EdgeType.PLATFORM_SELECTED
