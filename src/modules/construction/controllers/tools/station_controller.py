from modules.construction.controllers.tools.base_construction_tool_controller import BaseConstructionToolController
from shared.ui.utils.popups import user_input
from modules.construction.services.station_target import find_station_target
from core.models.railway.railway_system import RailwaySystem
from modules.construction.models.construction_state import ConstructionState
from modules.construction.views.station_view import StationView
from core.graphics.graphics_context import GraphicsContext
from core.models.event import Event
class StationController(BaseConstructionToolController):
    def __init__(self, railway: RailwaySystem, state: ConstructionState, graphics: GraphicsContext):
        view = StationView(railway, state, graphics)
        super().__init__(view, railway, state, graphics.camera)

    def process_event(self, event: Event) -> None:
        if event.button == 3:
            if self._construction_state.moving_station is not None:
                self._construction_state.moving_station = None
            else:
                self._construction_state.switch_mode(None)
            return

        target = find_station_target(self._railway, self._camera.screen_to_world(event.screen_pos), self._construction_state.moving_station)

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
        name = user_input()
        self._railway.stations.add(target.snapped, name)