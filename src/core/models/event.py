import pygame
from core.models.geometry.position import Position

class Event:
    def __init__(self, pygame_event: pygame.event.Event, screen_pos: Position, world_pos: Position, last_left_mouse_button_down_pos: Position | None = None, last_right_mouse_button_down_pos: Position | None = None):
        self.raw = pygame_event
        self.screen_pos = screen_pos
        self.world_pos = world_pos
        self.last_left_mouse_button_down_pos = last_left_mouse_button_down_pos
        self.last_right_mouse_button_down_pos = last_right_mouse_button_down_pos
        self.is_far_click = False
        
        if pygame_event.type == pygame.MOUSEBUTTONUP:
            if pygame_event.button == 1 and last_left_mouse_button_down_pos.distance_to(screen_pos) > 5:
                self.is_far_click = True
            elif pygame_event.button == 3 and last_right_mouse_button_down_pos.distance_to(screen_pos) > 5:
                self.is_far_click = True

    def __getattr__(self, name):
        return getattr(self.raw, name)
    
    @property
    def is_left_click(self) -> bool:
        return self.raw.type == pygame.MOUSEBUTTONUP and self.raw.button == 1
    
    @property
    def is_right_click(self) -> bool:
        return self.raw.type == pygame.MOUSEBUTTONUP and self.raw.button == 3