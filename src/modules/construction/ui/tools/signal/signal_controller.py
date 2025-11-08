from modules.construction.models.construction_tool_controller import ConstructionToolController
from .signal_target import find_signal_target, SignalTargetType
from modules.construction.models.construction_state import ConstructionState
from core.models.railway.railway_system import RailwaySystem
from .signal_view import SignalView
from core.graphics.graphics_context import GraphicsContext
from core.models.event import Event

class SignalController(ConstructionToolController):
    def __init__(self, railway: RailwaySystem, state: ConstructionState, graphics: GraphicsContext):
        view = SignalView(railway, state, graphics)
        super().__init__(view, railway, state, graphics.camera)

    def _on_click(self, event: Event) -> None:
        if event.is_right_click:
            self._construction_state.switch_tool(None)
            return

        target = find_signal_target(self._railway, self._camera.screen_to_world(event.screen_pos))

        if target.kind == SignalTargetType.TOGGLE:
            self._railway.signals.toggle(target.pose)

        elif target.kind == SignalTargetType.ADD:
            self._railway.signals.add(target.pose)