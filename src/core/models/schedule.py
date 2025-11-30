from operator import index
from typing import TYPE_CHECKING

from core.config.color import Color
from core.models.station import Station
if TYPE_CHECKING:
    from core.models.timetable import Timetable
    
class Schedule:
    color: Color
    timetable_code: str
    stops: list[dict[str, int]]
    index: int = 0
    
    
    def __init__(self, timetable: 'Timetable', start_time: int) -> 'Schedule':
        self.timetable_code = timetable.code
        self.color = timetable.color
        current_time = start_time
        self.stops: list[dict[str, int | None]] = [{
                    'station': timetable.stops[0]['station'],
                    'arrival_time': None,
                    'departure_time': start_time
                }]
        
        for stop in timetable.stops[1:-1]:
            travel_time = stop['travel_time']
            stop_time = stop['stop_time']
            arrival_time = current_time + travel_time
            departure_time = arrival_time + stop_time
            self.stops.append({
                'station': stop['station'],
                'arrival_time': arrival_time,
                'departure_time': departure_time
            })
            current_time = departure_time
            
        self.stops.append({
            'station': timetable.stops[-1]['station'],
            'arrival_time': current_time + timetable.stops[-1]['travel_time'],
            'departure_time': None
        })
        
        self.timetable_code = timetable.code
        
    def get_arrival_time(self) -> int | None:
        if self.index == 0:
            return None
        return self.stops[self.index]['arrival_time']
        
    def get_departure_time(self) -> int | None:
        if self.index >= len(self.stops):
            return None
        return self.stops[self.index]['departure_time']
    
    def depart_station(self) -> None:
        self.index += 1
        
    def get_next_station(self) -> Station:
        return self.stops[self.index]['station']
    
    def get_remaining_stops(self) -> list[dict]:
        """Returns a list of stop info dicts for rendering (current + next 2 stops)."""
        def format_time(minutes: int) -> str:
            return f"{minutes // 60:02d}:{minutes % 60:02d}"
        
        def format_stop(stop: dict) -> dict:
            station_name = stop['station'].name
            return {
                'station': station_name,
                'type': 'stop',
                'arrival': format_time(stop['arrival_time']) if stop['arrival_time'] is not None else 'DEP',
                'departure': format_time(stop['departure_time']) if stop['departure_time'] is not None else 'ARR',
            }
        
        return [format_stop(stop) for stop in self.stops[self.index:]]