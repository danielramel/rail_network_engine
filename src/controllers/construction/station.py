from models.construction import ConstructionState
from models.geometry import Position
from domain.rail_map import RailMap
from ui.popups import user_input
from services.construction.station_target import find_station_target

def handle_station_click(map: RailMap, world_pos: Position, state_info: ConstructionState):
    target = find_station_target(map, world_pos, state_info.moving_station)

    if not state_info.moving_station and target.hovered_station_pos is not None:
        state_info.moving_station = map.get_station_at(target.hovered_station_pos)
        return

    if target.blocked_by_node or target.overlaps_station:
        return

    if state_info.moving_station:
        map.move_station(state_info.moving_station.position, target.snapped)
        state_info.moving_station = None
        return

    name = user_input()
    map.add_station_at(target.snapped, name)