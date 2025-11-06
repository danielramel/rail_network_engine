"""
def draw_train_car(surface: pygame.Surface, edge: Edge, camera: Camera):
    a, b = edge
    ax, ay = camera.world_to_screen(a)
    bx, by = camera.world_to_screen(b)
    
    # Calculate direction vector
    dx, dy = bx - ax, by - ay
    length = math.sqrt(dx**2 + dy**2)
    
    if length == 0:
        return
    
    # Normalized direction and perpendicular vectors
    dir_x, dir_y = dx / length, dy / length
    perp_x, perp_y = -dir_y, dir_x
    
    # Rectangle width (perpendicular to the edge)
    width = 16 * camera.scale
    half_width = width / 2
    
    # Calculate the four corners of the rectangle
    points = [
        (ax + perp_x * half_width, ay + perp_y * half_width),
        (bx + perp_x * half_width, by + perp_y * half_width),
        (bx - perp_x * half_width, by - perp_y * half_width),
        (ax - perp_x * half_width, ay - perp_y * half_width)
    ]
    
    # Draw filled rectangle with border
    pygame.draw.polygon(surface, YELLOW, points)
    pygame.draw.polygon(surface, BLACK, points, 2)

def draw_train_lights(surface: pygame.Surface, world_pos: Position, direction: Direction,
                      camera: Camera, color: tuple):
    screen_x, screen_y = camera.world_to_screen(world_pos)

    # direction is a small vector like (dx, dy) with components in {-1, 0, 1}
    dx, dy = direction
    perp_x, perp_y = -dy, dx

    # spacing in screen pixels
    spacing = max(2, int(4 * camera.scale))
    radius = max(2, int(3 * camera.scale))

    left_x = int(screen_x + perp_x * -spacing)
    left_y = int(screen_y + perp_y * -spacing)
    right_x = int(screen_x + perp_x * spacing)
    right_y = int(screen_y + perp_y * spacing)


    pygame.draw.circle(surface, color, (left_x, left_y), radius)
    pygame.draw.circle(surface, color, (right_x, right_y), radius)


def draw_train(surface: pygame.Surface, train: Train, camera: Camera):
    if not train.path:
        return
    # Draw train cars
    occupied_edges = train.occupied_edges()
    for edge in occupied_edges:
        draw_train_car(surface, edge.move(edge.direction, train.edge_progress*GRID_SIZE), camera)

    last_edge = occupied_edges[-1]
    back_pos = last_edge.move(last_edge.direction, train.edge_progress*GRID_SIZE).a
    direction = last_edge.direction.opposite()
    draw_train_lights(surface, back_pos, direction, camera, color=RED)
    
    # draw current speed above the train front
    speed_text = f"{int(round(train.speed))} km/h"
    font_size = max(12, int(16 * camera.scale))
    font = pygame.font.SysFont(None, font_size)

    text_fg = font.render(speed_text, True, WHITE)
    text_bg = font.render(speed_text, True, BLACK)

    first_edge = occupied_edges[0]
    front_pos = first_edge.move(first_edge.direction, train.edge_progress*GRID_SIZE).b
    sx, sy = camera.world_to_screen(front_pos)
    offset_y = int(18 * camera.scale)

    bg_rect = text_bg.get_rect(center=(sx + 1, sy - offset_y + 1))
    fg_rect = text_fg.get_rect(center=(sx, sy - offset_y))

    surface.blit(text_bg, bg_rect)
    surface.blit(text_fg, fg_rect)
"""