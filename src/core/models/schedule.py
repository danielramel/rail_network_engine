from core.models.station import Station
from dataclasses import dataclass, field
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.models.railway.railway_system import RailwaySystem

@dataclass
class Schedule:
    code: str
    color: str
    first_train: int
    last_train: int
    frequency: int
    stops: list[dict[str, Station | int]] = field(default_factory=list)  # station, travel_time|None, stop_time|None

    def remove_station_from_stops(self, station_id: int):
        for stop in self.stops[:]:
            if stop['station'].id == station_id:
                self.stops.remove(stop)

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
    def from_dict(cls, data: dict, railway: 'RailwaySystem') -> 'Schedule':
        raw_stops = data['stops']
        stops: list[dict[str, Station | int]] = []

        # If persisted data already contains travel/stop, use directly
        if raw_stops and ('travel_time' in raw_stops[0] or 'stop_time' in raw_stops[0]):
            for entry in raw_stops:
                stops.append({
                    'station': railway.stations.get(entry['id']),
                    'travel_time': entry.get('travel_time'),
                    'stop_time': entry.get('stop_time')
                })
        else:
            # Backward compatibility: convert from arrival/departure fields
            prev_dep: int | None = None
            n = len(raw_stops)
            for i, entry in enumerate(raw_stops):
                station = railway.stations.get(entry['id'])
                arr = entry.get('arrival_time')
                dep = entry.get('departure_time')
                if i == 0:
                    stops.append({'station': station, 'travel_time': None, 'stop_time': None})
                    prev_dep = dep
                    continue
                travel = arr - prev_dep if (arr is not None and prev_dep is not None) else 0
                if i == n - 1:
                    stop = None
                else:
                    stop = (dep - arr) if (dep is not None and arr is not None) else 0
                    prev_dep = dep
                stops.append({'station': station, 'travel_time': travel, 'stop_time': stop})

        # Backwards compatibility: default color if missing
        color = data.get('color', 'RED')
        return cls(
            code=data['code'],
            color=color,
            first_train=data['first_train'],
            last_train=data['last_train'],
            frequency=data['frequency'],
            stops=stops
        )
