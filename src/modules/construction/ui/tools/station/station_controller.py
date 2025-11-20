from modules.construction.models.construction_tool_controller import ConstructionToolController
from core.models.geometry.position import Position
from .station_target import find_station_target
from core.models.railway.railway_system import RailwaySystem
from modules.construction.models.construction_state import ConstructionState
from .station_view import StationView
from core.graphics.graphics_context import GraphicsContext
from core.models.event import Event
class StationController(ConstructionToolController):
    def __init__(self, railway: RailwaySystem, state: ConstructionState, graphics: GraphicsContext):
        view = StationView(railway, state, graphics)
        super().__init__(view, railway, state, graphics)

    def _on_click(self, event: Event) -> None:
        if event.is_right_click:
            if self._construction_state.moving_station is not None:
                self._construction_state.moving_station = None
            else:
                self._construction_state.switch_tool(None)
            return

        target = find_station_target(self._railway, event.world_pos, self._construction_state.moving_station)

        # pick up a station if moving_station is None and mouse is over a station
        if not self._construction_state.moving_station and target.hovered_station_pos is not None:
            self._construction_state.moving_station = self._railway.stations.get_by_position(target.hovered_station_pos)
            return

        # blocked or overlapping -> do nothing
        elif target.blocked_by_node or target.overlaps_station:
            return

        # move station if one is being moved
        if self._construction_state.moving_station:
            self._railway.stations.move(self._construction_state.moving_station.id, target.snapped)
            self._construction_state.moving_station = None
            return

        # otherwise, create a new station
        self._input_component.prompt("Enter station name:", lambda name, pos=target.snapped: self._on_station_name_entered(name, pos))
        
    def _on_station_name_entered(self, name: str | None, pos: Position) -> None:
        if name is None or name.strip() == "":
            return
        self._railway.stations.add(pos, name)