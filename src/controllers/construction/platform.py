from models.map import RailMap
from models.geometry import Position
from config.settings import PLATFORM_LENGTH
from ui.popups import alert
from config.settings import GRID_SIZE


def handle_platform_click(map: RailMap, pos: Position, camera_scale, mode_info: dict):
    if mode_info['state'] == 'select_station':
        for station_pos in map.station_positions:
            if pos.is_within_station_rect(station_pos):
                map.add_platform_on(station_pos, list(mode_info['preview_edges']))
                break

        mode_info['state'] = None
        return
    
    closest_edge = pos.closest_edge(map.edges, camera_scale)
    if closest_edge is None:
        return
    if map.is_edge_platform(closest_edge):
        return
    
    edges = map.calculate_platform_preview(closest_edge)

    edge = next(iter(edges))
    if edge[0].distance_to(edge[1]) * len(edges) < PLATFORM_LENGTH * GRID_SIZE:
        alert(f'Platform too short! Minimum length is {PLATFORM_LENGTH} segments.')
        return
    
    mode_info['state'] = 'select_station'