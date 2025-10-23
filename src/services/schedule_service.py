from models.schedule import Schedule

class ScheduleService:
    def __init__(self):
        self._schedules : list[Schedule] = []

    def add_schedule(self, schedule: Schedule) -> None:
        self._schedules.append(schedule)

    def remove_schedule(self, schedule: Schedule) -> None:
        self._schedules.remove(schedule)

    def all_schedules(self) -> list[Schedule]:
        return self._schedules

    def get_schedule(self, index: int) -> Schedule:
        return self._schedules[index]