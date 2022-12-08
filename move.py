from dataclasses import dataclass


@dataclass
class Move:
    dx: float
    dy: float
    duration: int = 1
    own_speed: bool = False

    @property
    def pos(self):
        return self.dx, self.dy
