from core.models.schedule import Schedule
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.models.railway.railway_system import RailwaySystem

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
    
    def remove_station_from_all(self, station_id):
        for schedule in self._schedules:
            schedule.remove_station_from_stops(station_id)
    
    def to_dict(self) -> list[dict]:
        return [schedule.to_dict() for schedule in self._schedules]
    
    @classmethod
    def from_dict(cls, railway: 'RailwaySystem', data: list[dict]) -> 'ScheduleRepository':
        repo = cls()
        for schedule_data in data:
            schedule = Schedule.from_dict(schedule_data, railway)
            repo.add(schedule)
        return repo