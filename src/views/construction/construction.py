import pygame

from graphics.camera import Camera
from models.position import Position
from ui_elements.draw_utils import draw_station, draw_edges
from models.map import RailMap
from ui_elements import draw_construction_buttons, draw_zoom_indicator, draw_grid, draw_node, draw_signal

from config.colors import PURPLE
from models.construction import ConstructionState
from .signal import render_signal_preview
from .station import render_station_preview
from .rail import render_rail_preview
from .bulldoze import render_bulldoze_preview
from .platform import render_platform_preview
from models.construction import ConstructionMode


def render_construction_preview(surface: pygame.Surface, camera: Camera, map: RailMap, state: ConstructionState):
    draw_grid(surface, camera)

    draw_edges(surface, map.get_edges(), camera)
    for node in map.get_intersections():
        draw_node(surface, camera, node)
        
    for signal in map.get_signals():
        draw_signal(surface, camera, signal)
        
    for pos, name in map.stations.items():
        draw_station(surface, camera, pos, name)

    draw_edges(surface, map.get_platforms().keys(), camera, color=PURPLE)

    world_pos = camera.screen_to_world(Position(*pygame.mouse.get_pos()))
    if state.Mode == ConstructionMode.RAIL:
        render_rail_preview(surface, world_pos, state.construction_anchor, map, camera)
    elif state.Mode == ConstructionMode.SIGNAL:
        render_signal_preview(surface, world_pos, map, camera)
    elif state.Mode == ConstructionMode.STATION:
        render_station_preview(surface, world_pos, map, camera)
    elif state.Mode == ConstructionMode.PLATFORM:
        render_platform_preview(surface, world_pos, map, camera)
    elif state.Mode == ConstructionMode.BULLDOZE:
        render_bulldoze_preview(surface, world_pos, map, camera)
        
    draw_construction_buttons(surface, state)
    draw_zoom_indicator(surface, camera)