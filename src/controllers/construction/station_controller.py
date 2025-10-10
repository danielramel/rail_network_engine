from controllers.construction.base_construction_controller import BaseConstructionController
from models.event import CLICK_TYPE, Event
from ui.popups import user_input
from services.construction.station_target import find_station_target
from graphics.camera import Camera
from domain.rail_map import RailMap
from models.construction import ConstructionState
import pygame
from views.construction.station_view import StationView

class StationController(BaseConstructionController):
    def __init__(self, map: RailMap, state: ConstructionState, camera: Camera, screen: pygame.Surface):
        view = StationView(map, state, camera, screen)
        super().__init__(view, map, state, camera)
        
    def handle_event(self, event: Event):
        if event.click_type == CLICK_TYPE.RIGHT_CLICK:
            if self._construction_state.moving_station is not None:
                self._construction_state.moving_station = None
            else:
                self._construction_state.switch_mode(None)
            return

        target = find_station_target(self._map, self._camera.screen_to_world(event.screen_pos), self._construction_state.moving_station)

        # pick up a station if moving_station is None and mouse is over a station
        if not self._construction_state.moving_station and target.hovered_station_pos is not None:
            self._construction_state.moving_station = self._map.get_station_at(target.hovered_station_pos)
            return

        # blocked or overlapping -> do nothing
        if target.blocked_by_node or target.overlaps_station:
            return

        # move station if one is being moved
        if self._construction_state.moving_station:
            self._map.move_station(self._construction_state.moving_station.position, target.snapped)
            self._construction_state.moving_station = None
            return

        # otherwise, create a new station
        name = user_input()
        self._map.add_station_at(target.snapped, name)