from controllers.construction.base_construction_controller import BaseConstructionController
from models.event import Event, CLICK_TYPE
from services.construction.signal_target import find_signal_target
from graphics.camera import Camera
from domain.rail_map import RailMap
from models.construction import ConstructionState
import pygame
from views.construction.signal_view import SignalView

class SignalController(BaseConstructionController):
    def __init__(self, map: RailMap, state: ConstructionState, camera: Camera, screen: pygame.Surface):
        view = SignalView(map, state, camera, screen)
        super().__init__(view, map, state, camera)
        
    def handle_event(self, event: Event):
        if event.click_type != CLICK_TYPE.LEFT_CLICK:
            return False

        target = find_signal_target(self._map, event.world_pos)

        if target.kind == 'toggle':
            self._map.toggle_signal_at(target.snapped)
            return True

        elif target.kind == 'add':
            self._map.add_signal_at(target.snapped)
            return True

        return False