from core.models.railway.railway_system import RailwaySystem
from modules.setup.construction.models.construction_state import ConstructionState
from core.graphics.graphics_context import GraphicsContext
from modules.setup.construction.ui.construction_common_view import ConstructionCommonView
from modules.setup.construction.ui.tools.tunnel.tunnel_controller import TunnelController
from shared.ui.models.clickable_ui_component import ClickableUIComponent
from modules.setup.construction.models.construction_state import ConstructionTool
from core.models.geometry.position import Position
from .tools.rail.rail_controller import RailController
from .tools.platform.platform_controller import PlatformController
from .tools.signal.signal_controller import SignalController
from .tools.station.station_controller import StationController
from .tools.bulldoze.bulldoze_controller import BulldozeController
from modules.setup.construction.models.construction_tool_controller import ConstructionToolController
from shared.ui.models.full_screen_ui_component import FullScreenUIComponent


class ConstructionToolStrategy(ClickableUIComponent, FullScreenUIComponent):
    def __init__(self, railway: RailwaySystem, state: ConstructionState, graphics: GraphicsContext):
        self.view = ConstructionCommonView(railway, state, graphics)
        self._railway = railway
        self._state = state
        self._graphics = graphics

        self._controllers: dict[ConstructionTool, ConstructionToolController] = {
            ConstructionTool.RAIL: RailController(railway, state, graphics),
            ConstructionTool.TUNNEL: TunnelController(railway, state, graphics),
            ConstructionTool.SIGNAL: SignalController(railway, state, graphics),
            ConstructionTool.STATION: StationController(railway, state, graphics),
            ConstructionTool.PLATFORM: PlatformController(railway, state, graphics),
            ConstructionTool.BULLDOZE: BulldozeController(railway, state, graphics),
        }
        
    def _on_click(self, event) -> None:
        if self._state.tool is None:
            return
        
        self._controllers[self._state.tool].dispatch_event(event)
            
            
    def render(self, screen_pos: Position | None):
        self.view.render(screen_pos)
        if self._state.tool is None:
            return

        if self._state.tool is not None:
            self._controllers[self._state.tool].render(screen_pos)