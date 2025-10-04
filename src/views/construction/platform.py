from pygame import Surface
from config.colors import LIGHTBLUE, YELLOW
from graphics.camera import Camera
from models.map import RailMap
from ui.utils import draw_node, draw_station
from models.geometry import Position
from services.construction.platform_target import find_platform_target

def render_platform_preview(surface: Surface, world_pos: Position, mode_info: dict, map: RailMap, camera: Camera):
    for platform in map.get_platform_middle_points():
        draw_node(surface, platform, camera, color=YELLOW)

    if mode_info.get('state') == 'select_station':
        for station in map.station_positions:
            if world_pos.is_within_station_rect(station):
                draw_station(surface, map.get_station_at(station), camera, color=LIGHTBLUE)
                break
        return

    mode_info['preview_edges'].clear()
    mode_info['edge_type'] = None

    t = find_platform_target(map, world_pos, camera.scale)
    if t.kind in ('none', 'existing_platform'):
        draw_node(surface, world_pos, camera, color=LIGHTBLUE)
        return

    mode_info['preview_edges'] = t.edges
    mode_info['edge_type'] = 'red' if t.too_short else 'platform_preview'
