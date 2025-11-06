from shared.ui.models.ui_component import UIComponent
from core.graphics.camera import Camera
from core.models.event import Event
import pygame

class CameraController(UIComponent):
    def __init__(self, camera: Camera):
        self._camera = camera
        self._is_dragging = False
        
        
    def process_event(self, event: Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button in (1, 3):
            self._is_dragging = True
            self._camera.start_drag(event.screen_pos)

        elif event.type == pygame.MOUSEMOTION:
            if self._is_dragging:
                self._camera.update_drag(event.screen_pos)

        elif event.type == pygame.MOUSEWHEEL:
            self._camera.zoom(event.screen_pos, event.y)

        elif event.type == pygame.MOUSEBUTTONUP and event.button in (1, 3):
            was_dragging = self._is_dragging
            self._is_dragging = False
            epsilon_drag = self._camera.stop_drag(event.screen_pos)
            
            if not was_dragging or epsilon_drag:
                return False  # Not handled further
            
        return True
    
    def render(self, screen_pos):
        if screen_pos is None:
            self._is_dragging = False