from controllers.construction.base_construction_controller import BaseConstructionController
from services.construction.signal_target import find_signal_target, SignalTargetType
from graphics.camera import Camera
from models.railway_system import RailwaySystem
from models.construction_state import ConstructionState
from views.construction.signal_view import SignalView
from graphics.graphics_context import GraphicsContext
import pygame

class SignalController(BaseConstructionController):
    def __init__(self, railway: RailwaySystem, state: ConstructionState, graphics: GraphicsContext):
        view = SignalView(railway, state, graphics)
        super().__init__(view, railway, state, graphics.camera)

    def _handle_filtered_event(self, event: pygame.event.Event) -> None:
        if event.button == 3:
            self._construction_state.switch_mode(None)
            return

        target = find_signal_target(self._railway, self._camera.screen_to_world(event.screen_pos))

        if target.kind == SignalTargetType.TOGGLE:
            self._railway.signals.toggle(target.pose)

        elif target.kind == SignalTargetType.ADD:
            self._railway.signals.add(target.pose)