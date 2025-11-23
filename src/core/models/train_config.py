from dataclasses import dataclass, replace
from core.config.settings import Config

@dataclass
class TrainConfig:
    car_count: int = 6
    acceleration_in_m_s2: float = 1.2
    deceleration_in_m_s2: float = 1.4
    max_speed: int = 160
    acceleration: float = None
    deceleration: float = None

    @property
    def total_length(self) -> int:
        return (self.car_count * Config.TRAIN_CAR_LENGTH) + ((self.car_count - 1) * Config.TRAIN_CAR_GAP)
    
    def copy(self) -> 'TrainConfig':
        return replace(self, acceleration=self.acceleration_in_m_s2 * 3.6, deceleration=self.deceleration_in_m_s2 * 3.6)