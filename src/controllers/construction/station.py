from models.position import Position
from models.map import RailMap
from ui_elements.text_input import user_input

def handle_station_click(map: RailMap, pos: Position):
    snapped = pos.snap_to_grid()

    inp = user_input()
    
    if inp in map.stations.values():
        return # Station name must be unique

    for station_pos in map.stations.keys():
        if snapped.station_rect_overlaps(station_pos):
            return
        
    map.add_station_at(snapped, inp)