from config.colors import RED
from models.construction import ConstructionState
from models.geometry import Position
from models.map import RailMap
from ui.popups import user_input

def handle_station_click(map: RailMap, world_pos: Position, mode_info: dict):
    snapped = world_pos.snap_to_grid()
    moving_station = mode_info["moving_station"]
    if not moving_station:
        for station_pos in map.station_positions:
            if world_pos.is_within_station_rect(station_pos):
                mode_info["moving_station"] = map.get_station_at(station_pos)
                return

    if any(snapped.is_within_station_rect(node_pos) for node_pos in map.nodes):
        return
    elif any(snapped.station_rect_overlaps(station_pos) for station_pos in map.station_positions):
        return
    elif moving_station:
        map.remove_station_at(moving_station.position)
        map.add_station_at(snapped, moving_station.name)
        mode_info["moving_station"] = None
    else:
        name = user_input()
        map.add_station_at(snapped, name)