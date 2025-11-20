from modules.construction.models.construction_tool_controller import ConstructionToolController
from core.models.geometry.direction import Direction
from .rail_target import find_rail_target, RailTargetType
from core.models.geometry import Pose
from .rail_view import RailView
from core.graphics.graphics_context import GraphicsContext
from core.models.railway.railway_system import RailwaySystem
from modules.construction.models.construction_state import ConstructionState
from core.models.event import Event

class RailController(ConstructionToolController):
    def __init__(self, railway: RailwaySystem, state: ConstructionState, graphics: GraphicsContext):
        view = RailView(railway, state, graphics)
        super().__init__(view, railway, state, graphics)
        
        
    def _on_click(self, event: Event) -> None:
        if event.is_right_click:
            if self._construction_state.construction_anchor is not None:
                self._construction_state.construction_anchor = None
            else:
                self._construction_state.switch_tool(None)
            return
        
        target = find_rail_target(self._railway, event.world_pos, self._construction_state.construction_anchor)

        if target.kind == RailTargetType.NODE:
            if self._railway.signals.has_signal_at(target.snapped):
                signal = self._railway.signals.get(target.snapped)
                self._construction_state.construction_anchor = signal.pose
                return
            self._construction_state.construction_anchor = Pose(target.snapped, Direction(0, 0))

        elif target.kind == RailTargetType.ANCHOR_SAME:
            self._construction_state.construction_anchor = None


        elif target.kind == RailTargetType.PATH:
            self._railway.graph_service.add_segment(target.found_path, self._construction_state.track_speed, self._construction_state.track_length)
            self._construction_state.construction_anchor = Pose(
                target.snapped,
                target.found_path[-2].direction_to(target.snapped)
            )
