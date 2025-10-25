from dataclasses import dataclass

@dataclass(frozen=True)
class Direction:
    dx : int
    dy : int
    
    def get_opposite(self):
        return Direction(-self.dx, -self.dy)
    
    def __iter__(self):
        return iter((self.dx, self.dy))