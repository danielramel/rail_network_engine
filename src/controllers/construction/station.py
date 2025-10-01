from models.geometry import Position
from models.map import RailMap
from ui_elements.text_input import user_input

def handle_station_click(map: RailMap, pos: Position):
    snapped = pos.snap_to_grid()

    if any(snapped.within_station_rect(node_pos) for node_pos in map.nodes):
        return
    
    if any(snapped.station_rect_overlaps(station_pos) for station_pos in map.stations.keys()):
        return
        
    inp = user_input()
    
    map.add_station_at(snapped, inp)