from models.station import Station


from dataclasses import dataclass
@dataclass
class Train:
    """Represents a train with its type, route, schedule, and current state."""
    code: str  # e.g., "S70", "S71", "Z72"
    stations: list[Station]  # List of Station objects
    start_time: int  # e.g., 5 * 60 + 12
    frequency: int  # e.g., 20 (in minutes)


class TrainRepository:
    """In-memory repository for Train objects."""
    
    def __init__(self):
        self._trains: list[Train] = []
        self._mock_load()

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

        
    def _mock_load(self):
        """
        Loads mock timetable data into the repository.
        """
        self.timetable_data = [
            {
                "type": "S70",
                "stations": ["Hauptbahnhof", "Stadtmitte", "Ostbahnhof"],
                "start_time": "05:12",
                "frequency": "20 min"
            },
            {
                "type": "S71",
                "stations": ["Flughafen", "Messegelände", "Hauptbahnhof"],
                "start_time": "05:25",
                "frequency": "20 min"
            },
            {
                "type": "Z72",
                "stations": ["Nordstadt", "Zentrum", "...", "Südbahnhof"],
                "start_time": "06:00",
                "frequency": "30 min"
            },
            {
                "type": "S70",
                "stations": ["Westend", "Universitätsplatz", "...", "Endstation Ost"],
                "start_time": "05:30",
                "frequency": "15 min"
            },
            {
                "type": "Z72",
                "stations": ["Bahnhof Nord", "Altstadt", "...", "Industriegebiet"],
                "start_time": "06:15",
                "frequency": "30 min"
            }
        ]
        for entry in self.timetable_data:
            self.add(
                code=entry["type"],
                stations=entry["stations"],
                start_time=entry["start_time"],
                frequency=entry["frequency"]
            )