from pygame import Surface
from config.colors import LIGHTBLUE
from config.settings import GRID_SIZE, PLATFORM_LENGTH
from graphics.camera import Camera
from models.map import RailMap
from ui.utils import draw_node, draw_station
from services.construction.platform import get_platform_context
from models.geometry import Position
    

def render_platform_preview(surface: Surface, world_pos: Position, mode_info: dict, map: RailMap, camera: Camera):
    if mode_info['state'] == 'select_station':
        for station in map.station_positions:
            if world_pos.is_within_station_rect(station):
                draw_station(surface, map.get_station_at(station), camera, color=LIGHTBLUE)
                break
        return

    mode_info['preview_edges'].clear()
    mode_info['edge_type'] = None
    closest_edge = world_pos.closest_edge(map.edges, camera.scale)
    if closest_edge is None:
        draw_node(surface, world_pos, camera, color=LIGHTBLUE)
        return
    if map.is_edge_platform(closest_edge):
        draw_node(surface, world_pos, camera, color=LIGHTBLUE)
        return
    
    edges = map.calculate_platform_preview(closest_edge)
    mode_info['preview_edges'] = edges
    
    edge = next(iter(edges))
    if edge[0].distance_to(edge[1]) * len(edges) < PLATFORM_LENGTH * GRID_SIZE:
        mode_info['edge_type'] = 'red'
    else:
        mode_info['edge_type'] = 'platform_preview'