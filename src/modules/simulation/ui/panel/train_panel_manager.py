from shared.ui.models.ui_controller import UIController
from modules.simulation.ui.panel.train_panel import TrainPanel
from modules.simulation.models.simulation_state import SimulationState
from core.models.repositories.schedule_repository import ScheduleRepository
import pygame
from core.models.railway.railway_system import RailwaySystem


class TrainPanelManager(UIController):
    panels : dict[int, 'TrainPanel']
    
    def __init__(self, railway: RailwaySystem, simulation_state: SimulationState, screen: pygame.Surface, schedule_repository: ScheduleRepository):
        self.panels = {}
        self._railway = railway
        self._state = simulation_state
        self._schedule_repository = schedule_repository
        self._screen = screen
        
        self._state.selected_trains_callback = self.on_selected_trains_changed
    
    def on_selected_trains_changed(self, train_id, selected) -> None:
        if not selected:
            del self.panels[train_id]
            
        else:
            train = self._railway.trains.get(train_id)
            self.panels[train_id] = TrainPanel(train, self._screen, len(self.panels), self._schedule_repository, self.panel_closed)
            
        for index, panel in enumerate(self.panels.values()):
            panel.change_index(index)
            
    def panel_closed(self, train_id: int) -> None:
        self._state.deselect_train(train_id)
            
    @property
    def elements(self) -> tuple[TrainPanel]:
        return tuple(self.panels.values())