from models.station import Station

from dataclasses import dataclass
@dataclass
class Train:
    """Represents a train with its type, route, schedule, and current state."""
    code: str  # e.g., "S70", "S71", "Z72"
    first_train: int  # e.g., 5 * 60 + 12
    last_train: int  # e.g., 23 * 60 + 45
    frequency: int  # e.g., 20 (in minutes)
    schedule: list[dict[str, Station | int]] = None # List of dicts with 'station', 'arrival_time', 'departure_time'


class TrainRepository:
    """In-memory repository for Train objects."""
    
    def __init__(self):
        self._trains: list[Train] = []

    def add(self, train: Train) -> Train:
        """Add a new train to the repository."""
        self._trains.append(train)
    
    def remove(self, train: Train) -> None:
        """Remove a train from the repository."""
        self._trains.remove(train)
    
    def get(self, index: int) -> Train:
        """Get a train by its index in the list."""
        return self._trains[index]
    
    def all(self) -> list[Train]:
        """Return all trains."""
        return self._trains