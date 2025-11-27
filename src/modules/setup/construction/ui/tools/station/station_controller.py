from modules.setup.construction.models.construction_tool_controller import ConstructionToolController
from core.models.geometry.position import Position
from .station_target import StationTargetType, find_station_target
from core.models.railway.railway_system import RailwaySystem
from modules.setup.construction.models.construction_state import ConstructionState
from .station_view import StationView
from core.graphics.graphics_context import GraphicsContext
from core.models.event import Event
class StationController(ConstructionToolController):
    def __init__(self, railway: RailwaySystem, state: ConstructionState, graphics: GraphicsContext):
        view = StationView(railway, state, graphics)
        super().__init__(view, railway, state, graphics)

    def _on_click(self, event: Event) -> None:
        if event.is_right_click:
            if self._state.moving_station is not None:
                self._state.moving_station = None
            else:
                self._state.switch_tool(None)
            return

        target = find_station_target(self._railway, event.world_pos, self._state.moving_station)

        if target.kind is StationTargetType.HOVERED:
            self._state.moving_station = self._railway.stations.get_by_node(target.node)
            return
        
        if target.kind is StationTargetType.BLOCKED:
            message = "Cannot move station here!" if self._state.moving_station else "Cannot build station here!"
            self._graphics.alert_component.show_alert(message)
            return

        if self._state.moving_station:
            self._railway.stations.move(self._state.moving_station.id, target.node)
            self._state.moving_station = None
            return

        self._graphics.input_component.request_input("Enter station name:", lambda name, pos=target.node: self._on_station_name_entered(name, pos))
        
    def _on_station_name_entered(self, name: str | None, pos: Position) -> None:
        if name is None or name.strip() == "":
            return
        self._railway.stations.add(pos, name)