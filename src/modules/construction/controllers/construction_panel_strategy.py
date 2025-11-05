from modules.construction.construction_state import ConstructionState, ConstructionMode
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
        self._panels: dict[ConstructionMode, Panel] = {
            ConstructionMode.RAIL: RailPanel(screen, state),
            ConstructionMode.SIGNAL: SignalPanel(screen, state),
            ConstructionMode.STATION: StationPanel(screen, state),
            ConstructionMode.PLATFORM: PlatformPanel(screen, state),
            ConstructionMode.BULLDOZE: BulldozePanel(screen, state),
        }

    def render(self, screen_pos):
        if self._state.mode is None:
            return
        self._panels[self._state.mode].render(screen_pos)

    def process_event(self, event):
        if self._state.mode is None:
            return
        return self._panels[self._state.mode].dispatch_event(event)
    
    def contains(self, screen_pos):
        if self._state.mode is None:
            return False
        return self._panels[self._state.mode].contains(screen_pos)