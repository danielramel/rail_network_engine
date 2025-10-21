from models.station import Station


from dataclasses import dataclass
@dataclass
class Train:
    """Represents a train with its type, route, schedule, and current state."""
    code: str  # e.g., "S70", "S71", "Z72"
    stations: list[Station]
    start_time: int  # e.g., 5 * 60 + 12
    frequency: int  # e.g., 20 (in minutes)


class TrainRepository:
    """In-memory repository for Train objects."""
    
    def __init__(self):
        self._trains: list[Train] = []

    def add(self, code: str, stations: list[Station], start_time: int, frequency: int) -> Train:
        """Add a new train to the repository."""
        train = Train(code, stations, start_time, frequency)
        self._trains.append(train)
        return train
    
    def remove(self, train: Train) -> None:
        """Remove a train from the repository."""
        self._trains.remove(train)
    
    def get_by_index(self, index: int) -> Train:
        """Get a train by its index in the list."""
        return self._trains[index]
    
    def all(self) -> list[Train]:
        """Return all trains."""
        return self._trains