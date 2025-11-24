from typing import TYPE_CHECKING

from core.config.color import Color
from core.models.station import Station
if TYPE_CHECKING:
    from core.models.schedule import Schedule

    

class TimeTable:
    color: Color
    schedule_code: str
    stops: list[dict[str, int]]
    _station_index: int = 1
    
    
    def __init__(self, schedule: 'Schedule', start_time: int) -> 'TimeTable':
        self.schedule_code = schedule.code
        self.color = schedule.color
        current_time = start_time
        self.stops: list[dict[str, int | None]] = [{
                    'station': schedule.stops[0]['station'],
                    'arrival_time': None,
                    'departure_time': start_time
                }]
        
        for stop in schedule.stops[1:-1]:
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
            'station': schedule.stops[-1]['station'],
            'arrival_time': current_time + schedule.stops[-1]['travel_time'],
            'departure_time': None
        })
        
        self.schedule_code = schedule.code
        
        
    def get_next_station(self) -> Station:
        return self.stops[self._station_index]['station']
    
    def get_next_stop_str(self) -> str:
        def format_time(minutes: int) -> str:
            return f"{minutes // 60:02d}:{minutes % 60:02d}"
        
        if self._station_index == 0:
            return f"Departure from: {self.stops[0]['station'].name} at {format_time(self.stops[0]['departure_time'])}"
        
        return