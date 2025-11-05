from dataclasses import dataclass
import pygame
from graphics.camera import Camera

@dataclass
class GraphicsContext:
    screen: pygame.Surface
    camera: Camera