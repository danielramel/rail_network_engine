from models.geometry import Position
from models.map import RailMap
from ui.popups import user_input
from services.construction.station_target import find_station_target

def handle_station_click(map: RailMap, world_pos: Position, mode_info: dict):
    moving_station = mode_info.get("moving_station")
    target = find_station_target(map, world_pos, moving_station)

    if not moving_station and target.hovered_station_pos is not None:
        mode_info["moving_station"] = map.get_station_at(target.hovered_station_pos)
        return

    if target.blocked_by_node or target.overlaps_station:
        return

    if moving_station:
        map.remove_station_at(moving_station.position)
        map.add_station_at(target.snapped, moving_station.name)
        mode_info["moving_station"] = None
        return

    name = user_input()
    map.add_station_at(target.snapped, name)