from config.colors import RED
from models.construction import ConstructionState
from models.geometry import Position
from models.map import RailMap
from ui_elements.text_input import user_input

def handle_station_click(map: RailMap, world_pos: Position, construction_state: ConstructionState):
    snapped = world_pos.snap_to_grid()
    if not construction_state.moving_station:
        for station_pos in map.stations.keys():
            if world_pos.is_within_station_rect(station_pos):
                station = map.get_station_at(station_pos)
                map.remove_station_at(station.position)
                construction_state.moving_station = station
                return

    if any(snapped.is_within_station_rect(node_pos) for node_pos in map.nodes):
        return
    elif any(snapped.station_rect_overlaps(station_pos) for station_pos in map.stations.keys()):
        return
    elif construction_state.moving_station:
        map.add_station_at(snapped, construction_state.moving_station.name)
        construction_state.moving_station = None
    else:
        name = user_input()
        map.add_station_at(snapped, name)