from modules.setup.construction.models.construction_tool_controller import ConstructionToolController
from .platform_target import find_platform_target
from modules.setup.construction.models.construction_state import ConstructionState
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
                
        if len(self._railway.stations.all()) == 0:
            self._graphics.alert_component.show_alert('Please build a station first.')
            return

        target = find_platform_target(self._railway, event.world_pos, self._state.platform_edge_count, self._state.platform_waiting_for_station)
        
        if target.kind is PlatformTargetType.STATION_FOUND:
            self._railway.stations.add_platform(target.station.id, self._state.preview.edges)
            self._state.platform_waiting_for_station = False
            return
        
        if target.kind is PlatformTargetType.WAITING_FOR_STATION:
            self._state.platform_waiting_for_station = False
            return

        if target.kind is PlatformTargetType.NONE:
            return

        if target.kind is PlatformTargetType.INVALID:
            self._graphics.alert_component.show_alert(target.message)
            return

        self._state.platform_waiting_for_station = True
        self._state.preview.edge_action = EdgeAction.PLATFORM_SELECTED
