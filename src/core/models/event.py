import pygame
from core.models.geometry.position import Position

class Event:
    def __init__(self, pygame_event: pygame.event.Event, screen_pos: Position, world_pos: Position, last_mouse_button_down_pos: Position | None):
        self.raw = pygame_event
        self.screen_pos = screen_pos
        self.world_pos = world_pos
        self.is_far_click = pygame_event.type == pygame.MOUSEBUTTONUP and last_mouse_button_down_pos is not None and \
            last_mouse_button_down_pos.distance_to(screen_pos) > 5


    def __getattr__(self, name):
        return getattr(self.raw, name)
    
    @property
    def is_left_click(self) -> bool:
        return self.raw.type == pygame.MOUSEBUTTONUP and self.raw.button == 1
    
    @property
    def is_right_click(self) -> bool:
        return self.raw.type == pygame.MOUSEBUTTONUP and self.raw.button == 3