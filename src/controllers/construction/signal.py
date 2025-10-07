from models.geometry import Position
from domain.rail_map import RailMap
from services.construction.signal_target import find_signal_target

def handle_signal_click(map: RailMap, pos: Position):
    target = find_signal_target(map, pos)

    if target.kind == 'toggle':
        map.toggle_signal_at(target.snapped)
        
    elif target.kind == 'add':
        map.add_signal_at(target.snapped)