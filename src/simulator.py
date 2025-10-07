import pygame
from graphics.camera import Camera
from domain.rail_map import RailMap
from controllers.construction import handle_construction_events
from ui.construction.construction_buttons import ConstructionButtons
from ui.zoom_box import ZoomBox
from views.normal_view import handle_normal_events, render_normal_view
from views.construction import render_construction_preview
from models.construction import ConstructionState
from config.colors import BLACK
from ui.core.ui_layer import UILayer
from models.view import ViewMode
from ui.mode_selector_buttons import ModeSelectorButtons
from ui.construction.panels.construction_panel import ConstructionPanel

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
        pygame.display.set_caption("Rail Simulator")

        self.map = RailMap()
        self.camera = Camera()
        self.construction_state = ConstructionState()
        self.ui_layer = UILayer()
        self.view = ViewMode.CONSTRUCTION
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.ui_layer.add(
            ModeSelectorButtons(self.view),
            ZoomBox(self.screen, self.camera),
            ConstructionButtons(self.screen, self.construction_state),
            ConstructionPanel(self.screen, self.construction_state)
        )
        

    def handle_events(self):
        if self.view == ViewMode.CONSTRUCTION:
            return handle_construction_events(
                self.ui_layer,
                self.construction_state,
                self.camera,
                self.map
            )
        else:
            return handle_normal_events(
                self.screen,
                self.camera,
                self.map
            )

    def render_view(self):
        if self.view == ViewMode.CONSTRUCTION:
            render_construction_preview(self.ui_layer, self.screen, self.camera, self.map, self.construction_state)
        else:
            render_normal_view(self.screen, self.camera, self.map)

    # --- Main loop ---
    def run(self):
        while self.running:
            action = self.handle_events()
            if action == "quit":
                self.running = False
                
            self.screen.fill(BLACK)
            self.render_view()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
