import pygame
from enum import Enum
from camera import Camera
from rail_network import RailNetwork
from construction_view import handle_construction_view, render_construction_view
from normal_view import handle_normal_view, render_normal_view
from colors import *

class View(Enum):
    NORMAL = 0
    CONSTRUCTION = 1

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
pygame.display.set_caption("Rail Simulator")
network = RailNetwork()
camera = Camera()

button_size = 50
construction_toggle_button = pygame.Rect(10, 10, button_size, button_size)
font = pygame.font.SysFont(None, 40)
view = View.NORMAL
clock = pygame.time.Clock()
running = True


def draw_common_ui(surface):
    button_color = GREEN if view == View.CONSTRUCTION else GRAY
    pygame.draw.rect(surface, button_color, construction_toggle_button, border_radius=8)
    text_surface = font.render("C", True, WHITE)
    text_rect = text_surface.get_rect(center=construction_toggle_button.center)
    surface.blit(text_surface, text_rect)


while running:
    # Event handling
    if view == View.CONSTRUCTION:
        action = handle_construction_view(construction_toggle_button, screen, camera, network)
    elif view == View.NORMAL:
        action = handle_normal_view(construction_toggle_button, screen, camera, network)

    if action == "quit":
        running = False
    elif action == "toggle":
        view = View.NORMAL if view == View.CONSTRUCTION else View.CONSTRUCTION

    # Rendering
    screen.fill(BLACK)
    if view == View.CONSTRUCTION:
        render_construction_view(screen, camera, network)
    else:
        render_normal_view(screen, camera, network)

    draw_common_ui(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()