from dataclasses import dataclass

@dataclass(frozen=True, order=True)
class Direction:
    x : int
    y : int
    
    def get_opposite(self):
        return Direction(-self.x, -self.y)
    
    def get_cost(self) -> float:
        return 1.0 if self.x == 0 or self.y == 0 else 1.414
    
    def __iter__(self):
        return iter((self.x, self.y))