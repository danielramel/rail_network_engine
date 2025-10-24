from ui.models.base import UIComponent
import pygame
from graphics.camera import Camera

class CameraController(UIComponent):
    handled_events = [pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION, pygame.MOUSEWHEEL, pygame.MOUSEBUTTONUP]
    def __init__(self, camera: Camera):
        self._camera = camera
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._camera.start_drag(event.screen_pos)

        elif event.type == pygame.MOUSEMOTION:
            self._camera.update_drag(event.screen_pos)

        elif event.type == pygame.MOUSEWHEEL:
            self._camera.zoom(event.screen_pos, event.y)

        elif event.type == pygame.MOUSEBUTTONUP:
            was_dragging = self._camera.stop_drag(event.screen_pos)
            
            if not was_dragging:
                return False  # Not handled further
            
        return True