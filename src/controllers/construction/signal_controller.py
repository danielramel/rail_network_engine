from controllers.construction.base_construction_controller import BaseConstructionController
from services.construction.signal_target import find_signal_target, SignalTargetType
from graphics.camera import Camera
from models.railway_system import RailwaySystem
from models.construction_state import ConstructionState
import pygame
from views.construction.signal_view import SignalView

class SignalController(BaseConstructionController):
    def __init__(self, railway: RailwaySystem, state: ConstructionState, camera: Camera, screen: pygame.Surface):
        view = SignalView(railway, state, camera, screen)
        super().__init__(view, railway, state, camera)
        
    def handle_event(self, event: pygame.event.Event) -> None:
        if event.button == 3:
            self._construction_state.switch_mode(None)
            return

        target = find_signal_target(self._railway, self._camera.screen_to_world(event.screen_pos))

        if target.kind == SignalTargetType.TOGGLE:
            self._railway.signals.toggle(target.pose)

        elif target.kind == SignalTargetType.ADD:
            self._railway.signals.add(target.pose)