import pygame
from models.geometry import Position
    
from domain.rail_map import RailMap
from models.train import TrainRepository
from ui.components.base import BaseUIComponent
from views.timetable.timetable_view import TimetableView


class TimetableManager(BaseUIComponent):
    def __init__(self, map: RailMap, train_repository: TrainRepository, screen: pygame.Surface):
        self.view = TimetableView(map, train_repository, screen)
        self._map = map
        self._train_repository = train_repository

    def handle_event(self, event):
        return True
            
    def render(self, screen_pos: Position | None):
        self.view.render(screen_pos)

    def contains(self, screen_pos: Position) -> bool:
        return True