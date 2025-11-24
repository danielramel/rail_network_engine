from core.models.station import Station
from dataclasses import dataclass, field
from core.models.schedule import Schedule
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.models.railway.railway_system import RailwaySystem

@dataclass
class Route:
    code: str
    color: str
    first_train: int
    last_train: int
    frequency: int
    stops: list[dict[str, Station | int]] = field(default_factory=list)

    def remove_station_from_stops(self, station_id: int):
        for stop in self.stops[:]:
            if stop['station'].id == station_id:
                self.stops.remove(stop)
                
    def create_schedule(self, start_time: int) -> Schedule:
        return Schedule(self, start_time)

    def to_dict(self) -> dict:
        """Convert to serialisable dict used by repository persistence."""
        return {
            'code': self.code,
            'color': self.color,
            'first_train': self.first_train,
            'last_train': self.last_train,
            'frequency': self.frequency,
            'stops': [
                {
                    'id': entry['station'].id,
                    'travel_time': entry.get('travel_time'),
                    'stop_time': entry.get('stop_time')
                } for entry in self.stops
            ]
        }
        
    def get_full_travel_time(self) -> int:
        return sum(stop['travel_time']+stop['stop_time'] for stop in self.stops[1:-1]) + self.stops[-1]['travel_time']

    @classmethod
    def from_dict(cls, data: dict, railway: 'RailwaySystem') -> 'Route':
        
        stops: list[dict[str, Station | int]] = []

        for stop in data['stops']:
            stops.append({
                'station': railway.stations.get(stop['id']),
                'travel_time': stop["travel_time"],
                'stop_time': stop["stop_time"]
            })

        return cls(
            code=data['code'],
            color=data['color'],
            first_train=data['first_train'],
            last_train=data['last_train'],
            frequency=data['frequency'],
            stops=stops
        )
