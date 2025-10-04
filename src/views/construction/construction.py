import pygame

from graphics.camera import Camera
from models.geometry import Position
from ui.utils import draw_edge, draw_station,  draw_node, draw_signal, draw_grid
from models.map import RailMap

from config.colors import RED
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

    for *edge, data in map.edges.data():
        if state.is_edge_in_preview(edge):
            draw_edge(surface, edge, camera, edge_type=state.mode_info['edge_type'], speed=data['speed'])
        elif map.is_edge_platform(edge):
            draw_edge(surface, edge, camera, edge_type='platform')
        else:
            draw_edge(surface, edge, camera, speed=data['speed'])
        
    for node in map.junctions:
        draw_node(surface, node, camera)
        
    for signal in map.signals:
        if state.is_bulldoze_preview_node(signal.position):
            draw_signal(surface, signal, camera, color=RED)
        else:
            draw_signal(surface, signal, camera)

    for station in map.stations:
        if state.is_station_being_moved(station):
            continue
            
        draw_station(surface, station, camera)

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
        render_platform_preview(surface, world_pos, state.mode_info, map, camera)
    elif state.mode == ConstructionMode.BULLDOZE:
        render_bulldoze_preview(surface, world_pos, state.mode_info, map, camera)
        
    ui_layer.draw()

