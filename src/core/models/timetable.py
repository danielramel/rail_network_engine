from typing import TYPE_CHECKING

from core.config.color import Color
if TYPE_CHECKING:
    from core.models.schedule import Schedule

    

class TimeTable:
    color: Color
    schedule_code: str
    stops: list[dict[str, int]]
    
    
    def __init__(self, schedule: 'Schedule', start_time: int) -> 'TimeTable':
        self.schedule_code = schedule.code
        self.color = schedule.color
        current_time = start_time
        self.stops = [{
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
        
        
    def get_next_stop(self, index: int) -> dict[str, int] | None:
        return self.stops[index] if index < len(self.stops) else None