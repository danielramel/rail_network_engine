import pygame
from layer_handler import LayerHandler


class RailSimulator:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
        pygame.display.set_caption("Rail Simulator")
        self.clock = pygame.time.Clock()
        
        self.layer_handler = LayerHandler(self.screen)

    # --- Main loop ---
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                action = self.layer_handler.handle_event(event)
                if action == "quit":
                    running = False
                    break
                

            self.layer_handler.render_view()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
