import pygame

from graphics.camera import Camera
from models.geometry import Position
from ui.utils import draw_station, draw_edges, draw_node, draw_signal, draw_grid, color_from_speed
from models.map import RailMap

from config.colors import LIGHTBLUE
from models.construction import ConstructionState
from ui.core.ui_layer import UILayer
from .signal import render_signal_preview
from .station import render_station_preview
from .rail import render_rail_preview
from .bulldoze import render_bulldoze_preview
from .platform import render_platform_preview
from models.construction import ConstructionMode


def render_construction_preview(ui_layer: UILayer, surface: pygame.Surface, camera: Camera, map: RailMap, state: ConstructionState):
    draw_grid(surface, camera)

    for a, b, data in map.edges.data():
        if state.mode is ConstructionMode.BULLDOZE and ((a, b) in state.mode_info['hidden_edges'] or (b, a) in state.mode_info['hidden_edges']):
            continue
        pygame.draw.line(
            surface,
            color_from_speed(data['speed']),
            tuple(camera.world_to_screen(Position(*a))),
            tuple(camera.world_to_screen(Position(*b))),
            width=3
        )
        
    for node in map.junctions:
        draw_node(surface, node, camera)
        
    for signal in map.signals:
        draw_signal(surface, signal, camera)

    for station in map.stations:
        draw_station(surface, station, camera)

    draw_edges(surface, map.platforms.keys(), camera, color=LIGHTBLUE)

    pos = Position(*pygame.mouse.get_pos())
    world_pos = camera.screen_to_world(pos)
        
    if ui_layer.is_over_ui(pos):
        pass
    elif state.mode == ConstructionMode.RAIL:
        render_rail_preview(surface, world_pos, state.mode_info, map, camera)
    elif state.mode == ConstructionMode.SIGNAL:
        render_signal_preview(surface, world_pos, map, camera)
    elif state.mode == ConstructionMode.STATION:
        render_station_preview(surface, world_pos, state.mode_info, map, camera)
    elif state.mode == ConstructionMode.PLATFORM:
        render_platform_preview(surface, world_pos, map, camera)
    elif state.mode == ConstructionMode.BULLDOZE:
        render_bulldoze_preview(surface, world_pos, state.mode_info, map, camera)
        
    ui_layer.draw()

