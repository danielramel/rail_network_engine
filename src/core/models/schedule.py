from operator import index
from typing import TYPE_CHECKING

from core.config.color import Color
from core.models.station import Station
if TYPE_CHECKING:
    from core.models.route import Route

    

class Schedule:
    color: Color
    route_code: str
    stops: list[dict[str, int]]
    _station_index: int = 0
    
    
    def __init__(self, route: 'Route', start_time: int) -> 'Schedule':
        self.route_code = route.code
        self.color = route.color
        current_time = start_time
        self.stops: list[dict[str, int | None]] = [{
                    'station': route.stops[0]['station'],
                    'arrival_time': None,
                    'departure_time': start_time
                }]
        
        for stop in route.stops[1:-1]:
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
            'station': route.stops[-1]['station'],
            'arrival_time': current_time + route.stops[-1]['travel_time'],
            'departure_time': None
        })
        
        self.route_code = route.code
        
    def get_departure_time(self) -> int | None:
        if self._station_index >= len(self.stops):
            return None
        return self.stops[self._station_index]['departure_time']
    
    def depart_station(self) -> None:
        self._station_index += 1
        
    def get_next_station(self) -> Station:
        return self.stops[self._station_index]['station']
    
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
        
        return [format_stop(stop) for stop in self.stops[self._station_index:]]