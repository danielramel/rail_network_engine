import pygame

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
pygame.display.set_caption("Rail Simulator")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
GREEN = (0, 200, 0)

button_size = 50
button_rect = pygame.Rect(10, 10, button_size, button_size)
font = pygame.font.SysFont(None, 40)

construction_mode = False
clock = pygame.time.Clock()
running = True

def handle_construction_mode():
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            return "quit"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if button_rect.collidepoint(x, y):
                return "toggle"
            # Add construction-specific logic here
    return "continue"

while running:
    if construction_mode:
        action = handle_construction_mode()
        if action == "quit":
            running = False
        elif action == "toggle":
            construction_mode = False
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if button_rect.collidepoint(x, y):
                    construction_mode = True

    screen.fill(BLACK)
    button_color = GREEN if construction_mode else GRAY
    pygame.draw.rect(screen, button_color, button_rect, border_radius=8)
    text_surface = font.render("C", True, WHITE)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
