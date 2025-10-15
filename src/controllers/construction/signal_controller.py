from controllers.construction.base_construction_controller import BaseConstructionController
from models.event import Event, CLICK_TYPE
from services.construction.signal_target import find_signal_target, SignalTargetType
from graphics.camera import Camera
from domain.rail_map import RailMap
from models.construction import ConstructionState
import pygame
from views.construction.signal import SignalView

class SignalController(BaseConstructionController):
    def __init__(self, map: RailMap, state: ConstructionState, camera: Camera, screen: pygame.Surface):
        view = SignalView(map, state, camera, screen)
        super().__init__(view, map, state, camera)
        
    def handle_event(self, event: Event):
        if event.click_type == CLICK_TYPE.RIGHT_CLICK:
            self._construction_state.switch_mode(None)
            return

        target = find_signal_target(self._map, self._camera.screen_to_world(event.screen_pos))

        if target.kind == SignalTargetType.TOGGLE:
            self._map.toggle_signal_at(target.snapped)

        elif target.kind == SignalTargetType.ADD:
            self._map.add_signal_at(target.snapped)