import pygame
from enum import Enum
from construction_view import handle_construction_view, render_construction_view

class View(Enum):
    NORMAL = 0
    CONSTRUCTION = 1

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
pygame.display.set_caption("Rail Simulator")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
GREEN = (0, 200, 0)

button_size = 50
construction_toggle_button = pygame.Rect(10, 10, button_size, button_size)
font = pygame.font.SysFont(None, 40)

view = View.NORMAL
clock = pygame.time.Clock()
running = True

def render_normal_view(surface):
    # Stub for normal view rendering
    pass

def draw_common_ui(surface):
    button_color = GREEN if view == View.CONSTRUCTION else GRAY
    pygame.draw.rect(surface, button_color, construction_toggle_button, border_radius=8)
    text_surface = font.render("C", True, WHITE)
    text_rect = text_surface.get_rect(center=construction_toggle_button.center)
    surface.blit(text_surface, text_rect)

while running:
    # Event handling
    if view == View.CONSTRUCTION:
        action = handle_construction_view(construction_toggle_button)
        if action == "quit":
            running = False
        elif action == "toggle":
            view = View.NORMAL
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if construction_toggle_button.collidepoint(x, y):
                    view = View.CONSTRUCTION

    # Rendering
    screen.fill(BLACK)
    if view == View.CONSTRUCTION:
        render_construction_view(screen)
    else:
        render_normal_view(screen)

    draw_common_ui(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
