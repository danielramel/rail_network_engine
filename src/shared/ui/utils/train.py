import pygame

from core.graphics.camera import Camera
from core.config.color import Color
from core.models.train import Train
from enum import Enum, auto
from core.models.geometry.node import Node

class TRAINDRAWACTION(Enum):
    SHUTDOWN = auto()
    LIVE = auto()
    SCHEDULED = auto()
    SELECTED = auto()
    PREVIEWED = auto()
    REMOVE_PREVIEW = auto()

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
    elif action == TRAINDRAWACTION.REMOVE_PREVIEW:
        color = Color.RED
        
    
    
    distance = train._path_distance
    rail_i = 0
    rail = rails[rail_i]
    car_i = 0
    remainder = None
    while car_i < train.config.car_count:
        if distance >= rail.length:
            distance -= rail.length
            rail_i += 1
            rail = rails[rail_i]
        
        if remainder is not None:
            end = remainder / rail.length
            draw_train_car(screen, rail.edge.a, rail.edge.b, camera, color, 0.0, end)
            remainder = None
            car_i += 1
            continue
        
        start = distance / rail.length
        end = (distance + train.config.car_length) / rail.length
        draw_train_car(screen, rail.edge.a, rail.edge.b, camera, color, start, end)
        
        
        distance += train.config.car_length + train.config.car_gap
        if end > 1.0:
            remainder = (end - 1.0) * rail.length
            continue
        
        car_i += 1
        
def draw_train_car(
    screen: pygame.Surface,
    a: Node,
    b: Node,
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

    pygame.draw.aaline(screen, color, (dash_start_x, dash_start_y), (dash_end_x, dash_end_y), width)