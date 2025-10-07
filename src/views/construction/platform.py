from pygame import Surface
from config.colors import BLUE, LIGHTBLUE, YELLOW
from graphics.camera import Camera
from domain.rail_map import RailMap
from ui.utils import draw_node, draw_station, draw_dashed_line
from models.geometry import Position
from services.construction.platform_target import find_platform_target

def render_platform_preview(surface: Surface, world_pos: Position, mode_info: dict, map: RailMap, camera: Camera):
    if mode_info.get('state') == 'select_station':
        middle_point = map.get_middle_of_platform(mode_info['preview_edges'])
        for station_pos in map.station_positions:
            if world_pos.is_within_station_rect(station_pos):
                draw_station(surface, map.get_station_at(station_pos), camera, color=LIGHTBLUE)
                draw_dashed_line(surface, station_pos, middle_point, camera, color=LIGHTBLUE)
                break
        else:
            draw_dashed_line(surface, world_pos, middle_point, camera, color=LIGHTBLUE)
        return

    mode_info['preview_edges'].clear()
    mode_info['edge_type'] = None

    t = find_platform_target(map, world_pos, camera.scale)
    if t.kind in ('none', 'existing_platform'):
        draw_node(surface, world_pos, camera, color=BLUE)
        return

    mode_info['preview_edges'] = t.edges
    mode_info['edge_type'] = 'red' if t.too_short else 'platform'
