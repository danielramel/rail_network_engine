from domain.rail_map import RailMap
from models.geometry import Position
from config.settings import PLATFORM_LENGTH
from ui.popups import alert
from services.construction.platform_target import find_platform_target

def handle_platform_click(map: RailMap, pos: Position, camera_scale, mode_info: dict):
    if mode_info.get('state') == 'select_station':
        for station_pos in map.station_positions:
            if pos.is_within_station_rect(station_pos):
                map.add_platform_on(map.get_station_at(station_pos), list(mode_info['preview_edges']))
                break
        mode_info['state'] = None
        return

    target = find_platform_target(map, pos, camera_scale)
    if target.kind in ('none', 'existing_platform'):
        return

    if target.too_short:
        alert(f'Platform too short! Minimum length is {PLATFORM_LENGTH} segments.')
        return

    mode_info['state'] = 'select_station'
    mode_info['edge_type'] = 'platform_selected'
