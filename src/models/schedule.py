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
                    'id': entry['station'].id,
                    'arrival_time': entry['arrival_time'],
                    'departure_time': entry['departure_time']
                } for entry in self.stations
            ]
        }
        
    @classmethod
    def from_dict(cls, data: dict, simulation: 'Simulation') -> 'Schedule':
        """Create a Schedule object from a dictionary."""
        stations = []
        for entry in data['stations']:
            stations.append({
                'station': simulation.stations.get(entry['id']),
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
        
        
        
from models.schedule import Schedule

class ScheduleRepository:
    def __init__(self):
        self._schedules : list[Schedule] = []

    def add(self, schedule: Schedule) -> None:
        self._schedules.append(schedule)

    def remove(self, schedule: Schedule) -> None:
        self._schedules.remove(schedule)

    def all(self) -> list[Schedule]:
        return self._schedules

    def get(self, index: int) -> Schedule:
        return self._schedules[index]
    
    def to_dict(self) -> list[dict]:
        return [schedule.to_dict() for schedule in self._schedules]
    
    @classmethod
    def from_dict(cls, data: list[dict], simulation: 'Simulation') -> 'ScheduleRepository':
        repo = cls()
        for schedule_data in data:
            schedule = Schedule.from_dict(schedule_data, simulation)
            repo.add(schedule)
        return repo