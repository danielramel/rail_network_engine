from models.geometry.position import Position

class Train:
    """Represents a train with its type, route, schedule, and current state."""
    
    def __init__(self, train_type: str, stations: list[str], start_time: str, frequency: str):
        self.train_type = train_type  # e.g., "S70", "S71", "Z72"
        self.stations = stations  # List of station names
        self.start_time = start_time  # e.g., "05:12"
        self.frequency = frequency  # e.g., "20 min"
        self.current_position: Position | None = None
        self.current_station_index: int = 0
        self.is_active: bool = False
        
    def __repr__(self):
        return f"Train({self.train_type}, {self.stations[0]} → {self.stations[-1]})"


class TrainRepository:
    """In-memory repository for Train objects."""
    
    def __init__(self):
        self._trains: list[Train] = []
        self._next_id = 0
    
    def add(self, train_type: str, stations: list[str], start_time: str, frequency: str) -> Train:
        """Add a new train to the repository."""
        train = Train(train_type, stations, start_time, frequency)
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
    
    def get_active_trains(self) -> list[Train]:
        """Return only active trains currently running."""
        return [train for train in self._trains if train.is_active]
    
    def get_trains_by_type(self, train_type: str) -> list[Train]:
        """Return all trains of a specific type."""
        return [train for train in self._trains if train.train_type == train_type]
    
    def clear(self) -> None:
        """Remove all trains from the repository."""
        self._trains.clear()