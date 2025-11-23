from modules.construction.models.construction_tool_controller import ConstructionToolController
from .portal_target import PortalTargetType, find_portal_target
from modules.construction.models.construction_state import ConstructionState
from core.models.railway.railway_system import RailwaySystem
from core.models.event import Event
from .portal_view import PortalView
from core.graphics.graphics_context import GraphicsContext

class PortalController(ConstructionToolController):
    def __init__(self, railway: RailwaySystem, state: ConstructionState, graphics: GraphicsContext):
        view = PortalView(railway, state, graphics)
        super().__init__(view, railway, state, graphics)


    def _on_click(self, event: Event) -> None:
        if event.is_right_click:
            self._state.switch_tool(None)
            return

        target = find_portal_target(self._railway, event.world_pos)

        if target.kind is PortalTargetType.NONE:
            return

        if target.kind is PortalTargetType.INVALID:
            self._graphics.alert_component.show_alert(target.message)
            return
