from ui.construction.panels.bulldoze_panel import BulldozePanel
from ui.construction.panels.platform_panel import PlatformPanel
from ui.construction.panels.rail_panel import RailPanel
from ui.construction.panels.signal_panel import SignalPanel
from ui.construction.panels.station_panel import StationPanel
from models.construction_state import ConstructionMode, ConstructionState
from ui.models.panel import Panel
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