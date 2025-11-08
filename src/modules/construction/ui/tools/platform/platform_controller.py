from modules.construction.models.construction_tool_controller import ConstructionToolController
from shared.ui.utils.popups import alert
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
        super().__init__(view, railway, state, graphics.camera)


    def _on_click(self, event: Event) -> None:
        if event.button == 3:
            if self._construction_state.platform_waiting_for_station:
                self._construction_state.platform_waiting_for_station = False
            else:
                self._construction_state.switch_mode(None)
            return
                
        world_pos = self._camera.screen_to_world(event.screen_pos)
        # if user is currently selecting a station for the platform
        if self._construction_state.platform_waiting_for_station:
            for station in self._railway.stations.all():
                if world_pos.is_within_station_rect(station.position):
                    self._railway.stations.add_platform(station.id, list(self._construction_state.preview.edges))
                    break
            self._construction_state.platform_waiting_for_station = False
            return

        if len(self._railway.stations.all()) == 0:
            alert('Please build a station first.')
            self._construction_state.switch_mode(None)
            return

        target = find_platform_target(self._railway, world_pos, self._camera.scale)

        if target.kind in (PlatformTargetType.NONE, PlatformTargetType.EXISTING_PLATFORM):
            return

        if not target.is_valid:
            alert(f'Platform too short!')
            return

        # prepare to select station
        self._construction_state.platform_waiting_for_station = True
        self._construction_state.preview.edge_action = EdgeAction.PLATFORM_SELECTED
