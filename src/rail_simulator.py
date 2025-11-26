import pygame
from enum import Enum, auto
from shared.controllers.app_controller import AppController
from shared.controllers.main_menu_controller import MainMenuController
from shared.ui.models.ui_controller import UIController
from core.config.settings import Config
from PyQt6.QtWidgets import QApplication
import sys


class Phase(Enum):
    MENU = auto()
    SIMULATION = auto()


class SimulationManager:
    def __init__(self):
        pygame.init()
        
        self.qt_app = QApplication.instance() or QApplication(sys.argv)
        
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.key.set_repeat(500, 50)  # 500ms initial delay, 50ms between repeats, important for backspace
        pygame.display.set_caption("Rail Simulator")
        pygame.display.set_icon(pygame.image.load("src/assets/icons/app.png"))
        self.clock = pygame.time.Clock()
        
        self._current_state = Phase.MENU
        self._states: dict[Phase, UIController] = {
            Phase.MENU: MainMenuController(self.screen, self._start_simulation),
            Phase.SIMULATION: None
        }
        
        # If filepath provided via command line, skip menu
        if len(sys.argv) > 1:
            filepath = sys.argv[1]
            self._start_simulation(filepath)

    def _start_simulation(self, filepath: str | None = None):
        self._current_state = Phase.SIMULATION
        self._states[Phase.SIMULATION] = AppController(self.screen, self._exit_simulation, filepath)
        
    def _exit_simulation(self, message: str = None):
        self._current_state = Phase.MENU
        self._states[Phase.SIMULATION] = None
        if message:
            self._states[Phase.MENU].alert(message)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                
                self._states[self._current_state].dispatch_event(event)
            
            # Process Qt events without blocking (allows Qt windows to function)
            self.qt_app.processEvents()
            self._states[self._current_state].render()

            pygame.display.flip()
            self.clock.tick(Config.FPS)
            
            if self._current_state == Phase.SIMULATION:
                self._states[self._current_state].tick()

        pygame.quit()
