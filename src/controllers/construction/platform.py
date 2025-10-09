from domain.rail_map import RailMap
from models.construction import ConstructionState
from models.geometry import Position
from config.settings import PLATFORM_LENGTH
from ui.popups import alert
from services.construction.platform_target import find_platform_target

def handle_platform_click(map: RailMap, world_pos: Position, camera_scale, state: ConstructionState):
    if state.platform_state == 'select_station':
        for station_pos in map.station_positions:
            if world_pos.is_within_station_rect(station_pos):
                map.add_platform_on(map.get_station_at(station_pos), list(state.preview_edges))
                break
        state.platform_state = None
        return

    target = find_platform_target(map, world_pos, camera_scale)
    if target.kind in ('none', 'existing_platform'):
        return

    if not target.is_valid:
        alert(f'Platform too short! Minimum length is {PLATFORM_LENGTH} segments.')
        return

    state.platform_state = 'select_station'
    state.preview_edges_type = 'platform_selected'
