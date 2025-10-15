import pygame
from controllers.construction.base_construction_controller import BaseConstructionController
from models.event import CLICK_TYPE, Event
from services.construction.rail_target import find_rail_target, RailTargetType
from models.geometry import Pose
from views.construction.rail import RailView
from graphics.camera import Camera
from domain.rail_map import RailMap
from models.construction import ConstructionState

class RailController(BaseConstructionController):
    def __init__(self, map: RailMap, state: ConstructionState, camera: Camera, screen: pygame.Surface):
        view = RailView(map, state, camera, screen)
        super().__init__(view, map, state, camera)
        
        
    def handle_event(self, event: Event):
        if event.click_type == CLICK_TYPE.RIGHT_CLICK:
            if self._construction_state.construction_anchor is not None:
                self._construction_state.construction_anchor = None
            else:
                self._construction_state.switch_mode(None)
            return

        target = find_rail_target(self._map, self._camera.screen_to_world(event.screen_pos), self._construction_state.construction_anchor)
        if target.kind == RailTargetType.BLOCKED:
            return True  # event consumed, nothing happens

        if target.kind == RailTargetType.NODE:
            self._construction_state.construction_anchor = Pose(target.snapped, (0, 0))
            return True

        if target.kind == RailTargetType.ANCHOR_SAME:
            self._construction_state.construction_anchor = None
            return True

        if target.kind == RailTargetType.NO_PATH:
            return True  # consumed, but nothing changed

        if target.kind == RailTargetType.PATH:
            self._map.add_segment(target.found_path, self._construction_state.track_speed)
            self._construction_state.construction_anchor = Pose(
                target.snapped,
                target.found_path[-2].direction_to(target.snapped)
            )
            return True

        return False
