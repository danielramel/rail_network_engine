from models.geometry.position import Position
from models.station import Station
from dataclasses import dataclass, field
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.simulation import Simulation

@dataclass
class Schedule:
    """Represents a train with its type, route, schedule, and current state."""
    code: str  # e.g., "S70", "S71", "Z72"
    first_train: int  # e.g., 5 * 60 + 12
    last_train: int  # e.g., 23 * 60 + 45
    frequency: int  # e.g., 20 (in minutes)
    stations: list[dict[str, Station | int]] = field(default_factory=list)  # List of dicts with 'station', 'arrival_time', 'departure_time'
    
    def to_dict(self) -> dict:
        """Convert the Schedule object to a dictionary for serialization."""
        return {
            'code': self.code,
            'first_train': self.first_train,
            'last_train': self.last_train,
            'frequency': self.frequency,
            'stations': [
                {
                    'pos': entry['station'].position.to_dict(),
                    'arrival_time': entry['arrival_time'],
                    'departure_time': entry['departure_time']
                } for entry in self.stations
            ]
        }
        
    @classmethod
    def from_dict(cls, data: dict, rail_map: 'Simulation') -> 'Schedule':
        """Create a Schedule object from a dictionary."""
        stations = []
        for entry in data['stations']:
            station = rail_map.stations.get(Position.from_dict(entry['pos']))
            stations.append({
                'station': station,
                'arrival_time': entry['arrival_time'],
                'departure_time': entry['departure_time']
            })
        return cls(
            code=data['code'],
            first_train=data['first_train'],
            last_train=data['last_train'],
            frequency=data['frequency'],
            stations=stations
        )