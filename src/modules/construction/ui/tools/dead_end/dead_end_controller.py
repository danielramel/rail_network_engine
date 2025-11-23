from modules.construction.models.construction_tool_controller import ConstructionToolController
from .dead_end_target import DeadEndTargetType, find_dead_end_target
from modules.construction.models.construction_state import ConstructionState
from core.models.railway.railway_system import RailwaySystem
from core.models.event import Event
from .dead_end_view import DeadEndView
from core.graphics.graphics_context import GraphicsContext

class DeadEndController(ConstructionToolController):
    def __init__(self, railway: RailwaySystem, state: ConstructionState, graphics: GraphicsContext):
        view = DeadEndView(railway, state, graphics)
        super().__init__(view, railway, state, graphics)


    def _on_click(self, event: Event) -> None:
        if event.is_right_click:
            self._state.switch_tool(None)
            return

        target = find_dead_end_target(self._railway, event.world_pos)

        if target.kind is DeadEndTargetType.NONE:
            return

        if target.kind is DeadEndTargetType.INVALID:
            self._graphics.alert_component.show_alert(target.message)
            return
