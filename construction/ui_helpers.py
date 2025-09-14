import pygame
from enum import Enum

class ConstructionMode(Enum):
    RAIL = 'R'
    LIGHT = 'L'
    PLATFORM = 'P'

def get_zoom_box(surface: pygame.Surface) -> pygame.Rect:
    return pygame.Rect(surface.get_width() - 100, 10, 80, 30)

def get_construction_buttons(surface: pygame.Surface):
    button_size = 50
    button_margin = 10
    w, h = surface.get_size()
    buttons = []
    for i, mode in enumerate(ConstructionMode):
        rect = pygame.Rect(
            button_margin + i * (button_size + button_margin),
            h - button_size - button_margin,
            button_size,
            button_size
        )
        buttons.append((mode, rect))
    return buttons

