from dataclasses import dataclass

@dataclass(frozen=True, order=True)
class Direction:
    x : int
    y : int
    
    def opposite(self):
        return Direction(-self.x, -self.y)
    
    def __iter__(self):
        return iter((self.x, self.y))
    
    def is_zero(self) -> bool:
        return self.x == 0 and self.y == 0
    
    def get_valid_turns(self) -> list['Direction']:
        VALID_TURNS = {
            Direction(-1, -1): [Direction(-1, -1), Direction(-1, 0), Direction(0, -1)],
            Direction(-1, 1): [Direction(-1, 1), Direction(-1, 0), Direction(0, 1)],
            Direction(1, -1): [Direction(1, -1), Direction(1, 0), Direction(0, -1)],
            Direction(1, 1): [Direction(1, 1), Direction(1, 0), Direction(0, 1)],
            Direction(-1, 0): [Direction(-1, 0), Direction(-1, -1), Direction(-1, 1)],
            Direction(1, 0): [Direction(1, 0), Direction(1, -1), Direction(1, 1)],
            Direction(0, -1): [Direction(0, -1), Direction(-1, -1), Direction(1, -1)],
            Direction(0, 1): [Direction(0, 1), Direction(-1, 1), Direction(1, 1)],
            Direction(0, 0): [
                Direction(-1, -1), Direction(-1, 0), Direction(-1, 1),
                Direction(1, -1), Direction(1, 0), Direction(1, 1),
                Direction(0, -1), Direction(0, 1)
                ]
        }
        return VALID_TURNS[self]
    
    def to_dict(self) -> dict:
        return {
            "x": self.x,
            "y": self.y
        }