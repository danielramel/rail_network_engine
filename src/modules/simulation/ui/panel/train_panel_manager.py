from shared.ui.models.ui_controller import UIController
from modules.simulation.ui.panel.train_panel import TrainPanel
from modules.simulation.models.simulation_state import SimulationState
from core.models.repositories.timetable_repository import TimetableRepository
import pygame
import time
from core.models.railway.railway_system import RailwaySystem


class TrainPanelManager(UIController):
    panels : dict[int, 'TrainPanel']
    _panel_selected_at: dict[int, float]
    
    def __init__(self, railway: RailwaySystem, simulation_state: SimulationState, screen: pygame.Surface, timetable_repository: TimetableRepository):
        self.panels = {}
        self._panel_selected_at = {}
        self._railway = railway
        self._state = simulation_state
        self._timetable_repository = timetable_repository
        self._screen = screen
        self._state.subscribe_to_train_selected(self.on_train_selected)
        self._state.subscribe_to_train_deselected(self.on_train_deselected)
    
    def on_train_selected(self, train_id: int) -> None:
        if train_id not in self.panels:
            train = self._railway.trains.get(train_id)
            new_index = len(self.panels)
            
            if len(self.panels) >= 4:
                # Limit to 4 panels - remove the oldest one and use its index
                oldest_train_id = min(self._panel_selected_at, key=self._panel_selected_at.get)
                new_index = self.panels[oldest_train_id].index
                self._state.deselect_train(oldest_train_id)
            
            self.panels[train_id] = TrainPanel(train, self._screen, new_index, self._timetable_repository, self._state)
        
        # Update timestamp so this train becomes the youngest
        self._panel_selected_at[train_id] = time.time()
        
        for panel in self.panels.values():
            panel.deselect()
            
        self.panels[train_id].select()
            
    def on_train_deselected(self, train_id: int) -> None:
        del self.panels[train_id]
        del self._panel_selected_at[train_id]
            
    @property
    def elements(self) -> tuple[TrainPanel]:
        return tuple(self.panels.values())