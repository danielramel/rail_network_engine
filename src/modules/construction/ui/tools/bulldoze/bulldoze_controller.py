from core.models.railway.railway_system import RailwaySystem
from modules.construction.models.construction_state import ConstructionState
from core.graphics.graphics_context import GraphicsContext
from modules.construction.models.construction_tool_controller import ConstructionToolController
from .bulldoze_view import BulldozeView
from .bulldoze_target import BulldozeTargetType, find_bulldoze_target
from core.models.event import Event

class BulldozeController(ConstructionToolController):
    def __init__(self, railway: RailwaySystem, state: ConstructionState, graphics: GraphicsContext):
        view = BulldozeView(railway, state, graphics)
        super().__init__(view, railway, state, graphics)

    def _on_click(self, event: Event) -> bool:
        if event.is_right_click:
            self._state.switch_tool(None)
            return True
        
        target = find_bulldoze_target(self._railway, event.world_pos, self._graphics.camera.scale)
        if target.kind == BulldozeTargetType.SIGNAL:
            self._railway.signals.remove(target.position)
            return True
        elif target.kind == BulldozeTargetType.STATION:
            self._railway.stations.remove_station_at(target.position)
            return True
        elif target.kind == BulldozeTargetType.PLATFORM:
            self._railway.stations.remove_platform_at(target.edge)
            return True
        elif target.kind == BulldozeTargetType.SEGMENT:
            self._railway.graph_service.remove_segment(target.edges)
            return True
        return False