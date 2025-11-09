from core.models.station import Station
from dataclasses import dataclass, field
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.models.railway.railway_system import RailwaySystem

@dataclass
class Schedule:
    """Represents a train with its type, route, schedule, and current state."""
    code: str  # e.g., "S70", "S71", "Z72"
    first_train: int  # e.g., 5 * 60 + 12
    last_train: int  # e.g., 23 * 60 + 45
    frequency: int  # e.g., 20 (in minutes)
    stops: list[dict[str, Station | int]] = field(default_factory=list)  # List of dicts with 'station', 'arrival_time', 'departure_time'
    
    def remove_station_from_stops(self, station_id:int):
        for stop in self.stops[:]:
            if stop['station'].id == station_id:
                self.stops.remove(stop)
                
    def __repr__(self) -> str:
        return f"<Schedule {self.code} {self.first_train//60:02d}:{self.first_train%60:02d} - {self.last_train//60:02d}:{self.last_train%60:02d} every {self.frequency}m>"
    
    def to_dict(self) -> dict:
        """Convert the Schedule object to a dictionary for serialization."""
        return {
            'code': self.code,
            'first_train': self.first_train,
            'last_train': self.last_train,
            'frequency': self.frequency,
            'stops': [
                {
                    'id': entry['station'].id,
                    'arrival_time': entry['arrival_time'],
                    'departure_time': entry['departure_time']
                } for entry in self.stops
            ]
        }
        
    @classmethod
    def from_dict(cls, data: dict, railway: 'RailwaySystem') -> 'Schedule':
        """Create a Schedule object from a dictionary."""
        stops = []
        for entry in data['stops']:
            stops.append({
                'station': railway.stations.get(entry['id']),
                'arrival_time': entry['arrival_time'],
                'departure_time': entry['departure_time']
            })
        return cls(
            code=data['code'],
            first_train=data['first_train'],
            last_train=data['last_train'],
            frequency=data['frequency'],
            stops=stops
        )