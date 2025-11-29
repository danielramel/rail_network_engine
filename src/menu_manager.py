import pygame
from enum import Enum, auto
from shared.controllers.app_controller import AppController
from modules.home_page.home_page_screen import HomePageScreen
from shared.ui.models.ui_controller import UIController
from core.config.config import Config
from PyQt6.QtWidgets import QApplication
import sys


class MenuView(Enum):
    HOME_PAGE = auto()
    SIMULATION_PAGE = auto()


class MenuManager:
    def __init__(self):
        pygame.init()
        
        self.qt_app = QApplication.instance() or QApplication(sys.argv)
        
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.key.set_repeat(500, 50)  # 500ms initial delay, 50ms between repeats, important for backspace
        pygame.display.set_caption("Rail Simulator")
        pygame.display.set_icon(pygame.image.load("src/assets/icons/app.png"))
        self.clock = pygame.time.Clock()
        
        self._current_state = MenuView.HOME_PAGE
        self._states: dict[MenuView, UIController] = {
            MenuView.HOME_PAGE: HomePageScreen(self.screen, self._load_map),
            MenuView.SIMULATION_PAGE: None
        }
        
        if len(sys.argv) > 1:
            filepath = sys.argv[1]
            self._load_map(filepath)

    def _load_map(self, filepath: str | None = None):
        self._current_state = MenuView.SIMULATION_PAGE
        self._states[MenuView.SIMULATION_PAGE] = AppController(self.screen, self._exit_map, filepath)
        
    def _exit_map(self, message: str = None):
        self._current_state = MenuView.HOME_PAGE
        self._states[MenuView.SIMULATION_PAGE] = None
        if message:
            self._states[MenuView.HOME_PAGE].alert(message)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                # if event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_ESCAPE:
                #         running = False
                #         break
                
                self._states[self._current_state].dispatch_event(event)
            
            # Process Qt events without blocking (allows Qt windows to function)
            self.qt_app.processEvents()
            self._states[self._current_state].render()

            pygame.display.flip()
            self.clock.tick(Config.FPS)
            
            if self._current_state == MenuView.SIMULATION_PAGE:
                self._states[self._current_state].tick()

        pygame.quit()
