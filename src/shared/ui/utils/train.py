import pygame

from core.graphics.camera import Camera
from core.config.color import Color
from core.models.train import Train
from enum import Enum, auto
from core.models.geometry.position import Position
from core.config.settings import Settings

class TRAINDRAWACTION(Enum):
    SHUTDOWN = auto()
    LIVE = auto()
    SCHEDULED = auto()
    SELECTED = auto()
    PREVIEWED = auto()

def draw_train(screen: pygame.Surface, train: Train, camera: Camera, action: TRAINDRAWACTION) -> None:
    rails = train.get_occupied_rails()
    if action == TRAINDRAWACTION.SHUTDOWN:
        color = Color.DARKGREY
    elif action == TRAINDRAWACTION.LIVE:
        color = Color.WHITE
    elif action == TRAINDRAWACTION.SCHEDULED:
        color = train.timetable.color
    elif action == TRAINDRAWACTION.SELECTED:
        color = Color.ORANGE
    elif action == TRAINDRAWACTION.PREVIEWED:
        color = Color.YELLOW
        
    
    
    distance = train._path_distance
    rail_i = 0
    rail = rails[rail_i]
    car_i = 0
    remainder = None
    while car_i < Settings.TRAIN_CAR_COUNT:
        if distance >= rail.length:
            distance -= rail.length
            rail_i += 1
            rail = rails[rail_i]
        
        if remainder is not None:
            end = remainder / rail.length
            draw_occupied_edge(screen, rail.edge.a, rail.edge.b, camera, color, 0.0, end)
            remainder = None
            car_i += 1
            continue
        
        start = distance / rail.length
        end = (distance + Settings.TRAIN_CAR_LENGTH) / rail.length
        draw_occupied_edge(screen, rail.edge.a, rail.edge.b, camera, color, start, end)
        
        
        distance += Settings.TRAIN_CAR_LENGTH + Settings.TRAIN_CAR_GAP
        if end > 1.0:
            remainder = (end - 1.0) * rail.length
            continue
        
        car_i += 1
        
    return
        
    rail = rails[0]
    start = distance / rail.length
    end = (distance + 20) / rail.length
    draw_occupied_edge(screen, rail.edge.a, rail.edge.b, camera, color, start, end)
    remainder = rail.length - distance
    for rail in rails[1:-1]:
        draw_occupied_edge(screen, rail.edge.a, rail.edge.b, camera, color, 0.0, remainder - 0.1)
        start = distance / rail.length
        draw_occupied_edge(screen, rail.edge.a, rail.edge.b, camera, color, start, start + 0.9)
        remainder = rail.length - distance
        
    rail = rails[-1]
    draw_occupied_edge(screen, rail.edge.a, rail.edge.b, camera, color, 0.0, remainder - 0.1)
    
    
    return
    if edge_progress < 0.5:
        draw_occupied_edge(surface, edges[0].a, edges[0].b, camera, color, edge_progress+0.5, 1.0)
        draw_occupied_edge(surface, edges[1].a, edges[1].b, camera, color, 0.0, edge_progress)
        draw_occupied_edge(surface, edges[1].a, edges[1].b, camera, color, edge_progress+0.5, 1.0)
        for edge in edges[2:-2]:
            draw_occupied_edge(surface, edge.a, edge.b, camera, color, 0.0, edge_progress)
            draw_occupied_edge(surface, edge.a, edge.b, camera, color, edge_progress + 0.5, 1.0)
        draw_occupied_edge(surface, edges[-2].a, edges[-2].b, camera, color, 0.0, edge_progress)
        draw_occupied_edge(surface, edges[-2].a, edges[-2].b, camera, color, edge_progress + 0.5, 1.0)
        draw_occupied_edge(surface, edges[-1].a, edges[-1].b, camera, color, 0.0, edge_progress)
        
    else:
        draw_occupied_edge(surface, edges[0].a, edges[0].b, camera, color, edge_progress-0.5, edge_progress)
        for edge in edges[1:-1]:
            draw_occupied_edge(surface, edge.a, edge.b, camera, color, edge_progress - 0.5, edge_progress)
        draw_occupied_edge(surface, edges[-1].a, edges[-1].b, camera, color, edge_progress-0.5, edge_progress)
    


def draw_occupied_edge(
    surface: pygame.Surface,
    a: Position,
    b: Position,
    camera: Camera,
    color: tuple[int, int, int],
    start: float,
    end: float,
) -> None:
    if end - start <= 0.01:
        return
    
    if start < 0:
        start = 0
    if end > 1:
        end = 1

    a = camera.world_to_screen(a)
    b = camera.world_to_screen(b)
    (a_x, a_y), (b_x, b_y) = a, b
    dx = b_x - a_x
    dy = b_y - a_y

    dash_start_x = a_x + dx * start
    dash_start_y = a_y + dy * start
    dash_end_x = a_x + dx * end
    dash_end_y = a_y + dy * end

    width = max(3, int(10 * int(camera.scale)))

    pygame.draw.aaline(surface, color, (dash_start_x, dash_start_y), (dash_end_x, dash_end_y), width)