from core.models.timetable import Timetable
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.models.railway.railway_system import RailwaySystem

class TimetableRepository:
    def __init__(self, railway: 'RailwaySystem'):
        self._timetables : list[Timetable] = []
        self._railway = railway

    def add(self, timetable: Timetable) -> None:
        self._timetables.append(timetable)
        self._railway.mark_modified()

    def remove(self, timetable: Timetable) -> None:
        self._timetables.remove(timetable)
        self._railway.mark_modified()
        
    def all(self) -> list[Timetable]:
        return self._timetables

    def get(self, index: int) -> Timetable:
        return self._timetables[index]
    
    def remove_station_from_all(self, station_id):
        for timetable in self._timetables:
            timetable.remove_station_from_stops(station_id)
            
    def calculate_start_times(self) -> None:
        for timetable in self._timetables:
            timetable.calculate_start_times()
            
    def return_start_time(self, timetable_code: str, start_time: int) -> None:
        for timetable in self._timetables:
            if timetable.code == timetable_code:
                timetable.start_times.append(start_time)
                timetable.start_times.sort()
                return
    
    def to_dict(self) -> list[dict]:
        return [timetable.to_dict() for timetable in self._timetables]
    
    @classmethod
    def from_dict(cls, railway: 'RailwaySystem', data: list[dict]) -> 'TimetableRepository':
        repo = cls(railway)
        for timetable_data in data:
            timetable = Timetable.from_dict(timetable_data, railway)
            repo._timetables.append(timetable)  # bypass notification during loading
        return repo