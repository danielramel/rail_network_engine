from dataclasses import dataclass
import pygame
from core.graphics.camera import Camera
from shared.ui.components.alert_component import AlertComponent
from shared.ui.components.input_component import InputComponent

@dataclass
class GraphicsContext:
    screen: pygame.Surface
    camera: Camera
    alert_component: AlertComponent
    input_component: InputComponent