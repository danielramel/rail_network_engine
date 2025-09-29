import pygame
from enum import Enum
from graphics.camera import Camera
from models.map import RailMap
from controllers.construction import handle_construction_events
from views.normal_view import handle_normal_events, render_normal_view
from views.construction import render_construction_preview
from models.construction import ConstructionState
from config.colors import WHITE, BLACK, GRAY, GREEN
from ui_elements.buttons import load_construction_icons

class View(Enum):
    NORMAL = 0
    CONSTRUCTION = 1

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
        pygame.display.set_caption("Rail Simulator")

        self.map = RailMap()
        self.camera = Camera()
        self.construction_state = ConstructionState()
        self.view = View.CONSTRUCTION
        self.clock = pygame.time.Clock()
        self.running = True

        self.button_size = 50
        self.construction_toggle_button = pygame.Rect(10, 10, self.button_size, self.button_size)
        self.font = pygame.font.SysFont(None, 40)
        
        self.construction_icon_cache = load_construction_icons()
        

    def draw_common_ui(self):
        button_color = GREEN if self.view == View.CONSTRUCTION else GRAY
        pygame.draw.rect(self.screen, button_color, self.construction_toggle_button, border_radius=8)
        text_surface = self.font.render("C", True, WHITE)
        text_rect = text_surface.get_rect(center=self.construction_toggle_button.center)
        self.screen.blit(text_surface, text_rect)

    def handle_events(self):
        if self.view == View.CONSTRUCTION:
            return handle_construction_events(
                self.construction_state,
                self.construction_toggle_button,
                self.screen,
                self.camera,
                self.map
            )
        else:
            return handle_normal_events(
                self.construction_toggle_button,
                self.screen,
                self.camera,
                self.map
            )

    def render_view(self):
        if self.view == View.CONSTRUCTION:
            render_construction_preview(self.screen, self.camera, self.map, self.construction_state, self.construction_icon_cache)
        else:
            render_normal_view(self.screen, self.camera, self.map)

    # --- Main loop ---
    def run(self):
        while self.running:
            action = self.handle_events()
            if action == "quit":
                self.running = False
            elif action == "toggle":
                self.view = View.NORMAL if self.view == View.CONSTRUCTION else View.CONSTRUCTION

            self.screen.fill(BLACK)
            self.render_view()
            self.draw_common_ui()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
