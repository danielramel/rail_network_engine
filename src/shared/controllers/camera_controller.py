from ui.models.ui_component import UIComponent
import pygame
from graphics.camera import Camera

class CameraController(UIComponent):
    handled_events = [pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION, pygame.MOUSEWHEEL, pygame.MOUSEBUTTONUP]
    def __init__(self, camera: Camera):
        self._camera = camera
        
    def dispatch_event(self, event):
        return super().dispatch_event(event, mouse_event_filter=False)
        
    def process_event(self, event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button in (1, 3):
            self._camera.start_drag(event.screen_pos)

        elif event.type == pygame.MOUSEMOTION:
            self._camera.update_drag(event.screen_pos)

        elif event.type == pygame.MOUSEWHEEL:
            self._camera.zoom(event.screen_pos, event.y)

        elif event.type == pygame.MOUSEBUTTONUP and event.button in (1, 3):
            was_dragging = self._camera.stop_drag(event.screen_pos)
            
            if not was_dragging:
                return False  # Not handled further
            
        return True