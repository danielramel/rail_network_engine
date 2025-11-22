from modules.construction.models.construction_tool_controller import ConstructionToolController
from .platform_target import find_platform_target
from modules.construction.models.construction_state import ConstructionState
from core.models.railway.railway_system import RailwaySystem
from core.models.event import Event
from .platform_view import PlatformView, PlatformTargetType
from core.graphics.graphics_context import GraphicsContext
from shared.ui.enums.edge_action import EdgeAction

class PlatformController(ConstructionToolController):
    def __init__(self, railway: RailwaySystem, state: ConstructionState, graphics: GraphicsContext):
        view = PlatformView(railway, state, graphics)
        super().__init__(view, railway, state, graphics)


    def _on_click(self, event: Event) -> None:
        if event.is_right_click:
            if self._state.platform_waiting_for_station:
                self._state.platform_waiting_for_station = False
            else:
                self._state.switch_tool(None)
            return
                
        # if user is currently selecting a station for the platform
        if self._state.platform_waiting_for_station:
            for station in self._railway.stations.all():
                if event.world_pos.is_within_station_rect(station.position):
                    self._railway.stations.add_platform(station.id, self._state.preview.edges)
                    break
            self._state.platform_waiting_for_station = False
            return

        if len(self._railway.stations.all()) == 0:
            self._alert_component.show_alert('Please build a station first.')
            return

        target = find_platform_target(self._railway, event.world_pos, self._camera.scale, self._state.platform_edge_count)

        if target.kind is PlatformTargetType.NONE:
            return

        if target.kind is PlatformTargetType.INVALID:
            self._alert_component.show_alert(target.message)
            return

        # prepare to select station
        self._state.platform_waiting_for_station = True
        self._state.preview.edge_action = EdgeAction.PLATFORM_SELECTED
