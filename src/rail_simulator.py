import pygame
from shared.controllers.app_controller import AppController
from core.config.settings import FPS
from PyQt6.QtWidgets import QApplication
import sys


class RailSimulator:
    def __init__(self):
        pygame.init()
        
        # Initialize QApplication in main thread (required for Qt)
        self.qt_app = QApplication.instance() or QApplication(sys.argv)
        
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.key.set_repeat(500, 50)  # 500ms initial delay, 50ms between repeats
        pygame.display.set_caption("Rail Simulator")
        self.clock = pygame.time.Clock()
        
        self.app_controller = AppController(self.screen)

    # --- Main loop ---
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                action = self.app_controller.dispatch_event(event)
                if action == "quit":
                    running = False
                    break
            
            # Process Qt events without blocking (allows Qt windows to function)
            self.qt_app.processEvents()

            self.app_controller.render()

            pygame.display.flip()
            self.clock.tick(FPS)
            self.app_controller.tick()

        pygame.quit()
