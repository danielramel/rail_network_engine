from shared.ui.models.ui_controller import UIController
from modules.simulation.ui.panel.train_panel import TrainPanel
from modules.simulation.models.simulation_state import SimulationState
from core.models.repositories.route_repository import RouteRepository
import pygame
from core.models.railway.railway_system import RailwaySystem


class TrainPanelManager(UIController):
    panels : dict[int, 'TrainPanel']
    
    def __init__(self, railway: RailwaySystem, simulation_state: SimulationState, screen: pygame.Surface, route_repository: RouteRepository):
        self.panels = {}
        self._railway = railway
        self._state = simulation_state
        self._route_repository = route_repository
        self._screen = screen
        self._state.subscribe_to_train_selected(self.on_train_selected)
        self._state.subscribe_to_train_deselected(self.on_train_deselected)
    
    def on_train_selected(self, train_id: int) -> None:
        if train_id not in self.panels:
            train = self._railway.trains.get(train_id)
            self.panels[train_id] = TrainPanel(train, self._screen, len(self.panels), self._route_repository, self._state)
            
        for index, panel in enumerate(self.panels.values()):
            panel.deselect()
            panel.change_index(index)
            
        self.panels[train_id].select()
            
    def on_train_deselected(self, train_id: int) -> None:
        del self.panels[train_id]
        for index, panel in enumerate(self.panels.values()):
            panel.change_index(index)
            
    @property
    def elements(self) -> tuple[TrainPanel]:
        return tuple(self.panels.values())