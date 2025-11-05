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
    def from_dict(cls, simulation: 'RailwaySystem', data: list[dict]) -> 'ScheduleRepository':
        repo = cls()
        for schedule_data in data:
            schedule = Schedule.from_dict(schedule_data, simulation)
            repo.add(schedule)
        return repo