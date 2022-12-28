from dataclasses import dataclass

from utils import normalize


@dataclass
class Move:
    dx: float
    dy: float
    duration: int = 1
    own_speed: bool = False
    normalize: bool = False

    def __post_init__(self):
        if self.normalize or self.own_speed:
            self.dx, self.dy = normalize(*self.pos)

    @property
    def vector(self):
        return self.dx, self.dy

    @property
    def pos(self):
        return self.dx, self.dy

    def update(self):
        self.duration -= 1

    def amplify(self, amount):
        self.dx *= amount
        self.dy *= amount
