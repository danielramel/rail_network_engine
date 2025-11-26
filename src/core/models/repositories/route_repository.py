from core.models.route import Route
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.models.railway.railway_system import RailwaySystem

class RouteRepository:
    def __init__(self, railway: 'RailwaySystem'):
        self._routes : list[Route] = []
        self._railway = railway

    def add(self, route: Route) -> None:
        self._routes.append(route)
        self._railway.mark_modified()

    def remove(self, route: Route) -> None:
        self._routes.remove(route)
        self._railway.mark_modified()
        
    def all(self) -> list[Route]:
        return self._routes

    def get(self, index: int) -> Route:
        return self._routes[index]
    
    def remove_station_from_all(self, station_id):
        for route in self._routes:
            route.remove_station_from_stops(station_id)
    
    def to_dict(self) -> list[dict]:
        return [route.to_dict() for route in self._routes]
    
    @classmethod
    def from_dict(cls, railway: 'RailwaySystem', data: list[dict]) -> 'RouteRepository':
        repo = cls(railway)
        for route_data in data:
            route = Route.from_dict(route_data, railway)
            repo._routes.append(route)  # bypass notification during loading
        return repo