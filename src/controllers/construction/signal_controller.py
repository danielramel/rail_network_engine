from controllers.construction.base_construction_controller import BaseConstructionController
from services.construction.signal_target import find_signal_target, SignalTargetType
from graphics.camera import Camera
from models.simulation import Simulation
from models.construction import ConstructionState
import pygame
from views.construction.signal import SignalView

class SignalController(BaseConstructionController):
    def __init__(self, simulation: Simulation, state: ConstructionState, camera: Camera, screen: pygame.Surface):
        view = SignalView(simulation, state, camera, screen)
        super().__init__(view, simulation, state, camera)
        
    def handle_event(self, event: pygame.event.Event) -> None:
        if event.button == 3:
            self._construction_state.switch_mode(None)
            return

        target = find_signal_target(self._simulation, self._camera.screen_to_world(event.screen_pos))

        if target.kind == SignalTargetType.TOGGLE:
            self._simulation.signals.toggle(target.snapped)

        elif target.kind == SignalTargetType.ADD:
            self._simulation.signals.add(target.snapped)