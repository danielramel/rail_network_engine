from modules.setup.construction.models.construction_tool_controller import ConstructionToolController
from core.models.geometry.direction import Direction
from .track_target import find_track_target, TrackTargetType
from core.models.geometry.pose import Pose
from .track_view import TrackView
from core.graphics.graphics_context import GraphicsContext
from core.models.railway.railway_system import RailwaySystem
from modules.setup.construction.models.construction_state import ConstructionState
from core.models.event import Event

class TrackController(ConstructionToolController):
    def __init__(self, railway: RailwaySystem, state: ConstructionState, graphics: GraphicsContext):
        view = TrackView(railway, state, graphics)
        super().__init__(view, railway, state, graphics)
        
        
    def _on_click(self, event: Event) -> None:
        if event.is_right_click:
            if self._state.construction_anchor is not None:
                self._state.construction_anchor = None
            else:
                self._state.switch_tool(None)
            return
        
        target = find_track_target(self._railway, event.world_pos, self._state.construction_anchor)
        
        if target.kind is TrackTargetType.BLOCKED:
            self._graphics.alert_component.show_alert("Position blocked!")
        
        elif target.kind is TrackTargetType.NO_PATH:
            self._graphics.alert_component.show_alert("No path found!")
        
        elif target.kind is TrackTargetType.ANCHOR_SAME:
            self._state.construction_anchor = None

        elif target.kind is TrackTargetType.ANCHOR:
            self._state.construction_anchor = target.anchor

        elif target.kind is TrackTargetType.PATH:
            self._railway.graph_service.add_section(target.found_path, self._state.track_speed, self._state.track_length)
            self._state.construction_anchor = Pose(
                target.node,
                target.found_path[-2].direction_to(target.node)
            )
