from modules.construction.models.construction_state import ConstructionState, ConstructionTool
from shared.ui.models.panel import Panel
from modules.construction.ui.panels.rail_panel import RailPanel
from modules.construction.ui.panels.signal_panel import SignalPanel
from modules.construction.ui.panels.station_panel import StationPanel
from modules.construction.ui.panels.platform_panel import PlatformPanel
from modules.construction.ui.panels.bulldoze_panel import BulldozePanel
import pygame


class ConstructionPanelStrategy(Panel):
    def __init__(self, screen: pygame.Surface, state: ConstructionState):
        self._state = state
        self._panels: dict[ConstructionTool, Panel] = {
            ConstructionTool.RAIL: RailPanel(screen, state),
            ConstructionTool.SIGNAL: SignalPanel(screen, state),
            ConstructionTool.STATION: StationPanel(screen, state),
            ConstructionTool.PLATFORM: PlatformPanel(screen, state),
            ConstructionTool.BULLDOZE: BulldozePanel(screen, state),
        }

    def render(self, screen_pos):
        if self._state.tool is None:
            return
        self._panels[self._state.tool].render(screen_pos)

    def process_event(self, event):
        if self._state.tool is None:
            return
        return self._panels[self._state.tool].dispatch_event(event)
    
    def contains(self, screen_pos):
        if self._state.tool is None:
            return False
        return self._panels[self._state.tool].contains(screen_pos)