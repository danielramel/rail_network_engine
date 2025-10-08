from pygame import Surface
from config.colors import BLUE, LIGHTBLUE, YELLOW
from graphics.camera import Camera
from domain.rail_map import RailMap
from models.construction import ConstructionState
from ui.utils import draw_node, draw_station, draw_dotted_line
from models.geometry import Position
from services.construction.platform_target import find_platform_target

def render_platform_preview(surface: Surface, world_pos: Position, state: ConstructionState, map: RailMap, camera: Camera):
    if state.platform_state == 'select_station':
        middle_point = map.get_middle_of_platform(state.preview_edges)
        for station_pos in map.station_positions:
            if world_pos.is_within_station_rect(station_pos):
                draw_station(surface, map.get_station_at(station_pos), camera, color=LIGHTBLUE)
                draw_dotted_line(surface, station_pos, middle_point, camera, color=LIGHTBLUE)
                break
        else:
            draw_dotted_line(surface, world_pos, middle_point, camera, color=LIGHTBLUE)
        return

    state.preview_edges.clear()
    state.preview_edges_type = None

    t = find_platform_target(map, world_pos, camera.scale)
    if t.kind in ('none', 'existing_platform'):
        draw_node(surface, world_pos, camera, color=BLUE)
        return

    state.preview_edges = t.edges
    state.preview_edges_type = 'platform' if t.is_valid else 'invalid_platform'
