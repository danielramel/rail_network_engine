import pygame
from controllers.ui_controller import ConstructionModeController
from models.event import CLICK_TYPE, Event
from services.construction.rail_target import find_rail_target
from models.geometry import Pose
from views.construction.rail import RailView
from graphics.camera import Camera
from domain.rail_map import RailMap
from models.construction import ConstructionState

class RailController(ConstructionModeController):
    def __init__(self, map: RailMap, state: ConstructionState, camera: Camera, screen: pygame.Surface):
        view = RailView(map, state, camera, screen)
        super().__init__(view, map, state, camera)
        
        
    def handle_event(self, event: Event):
        if event.click_type == CLICK_TYPE.RIGHT_CLICK:
            if self._construction_state.construction_anchor is not None:
                self._construction_state.construction_anchor = None
                return True
            return False

        target = find_rail_target(self._map, event.world_pos, self._construction_state.construction_anchor)
        if target.kind == 'blocked':
            return True  # event consumed, nothing happens

        if target.kind == 'node':
            self._construction_state.construction_anchor = Pose(target.snapped, (0, 0))
            return True

        if target.kind == 'anchor_same':
            self._construction_state.construction_anchor = None
            return True

        if target.kind == 'no_path':
            return True  # consumed, but nothing changed

        if target.kind == 'path':
            self._map.add_segment(target.found_path, self._construction_state.track_speed)
            self._construction_state.construction_anchor = Pose(
                target.snapped,
                target.found_path[-2].direction_to(target.snapped)
            )
            return True

        return False
