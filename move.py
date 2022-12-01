from dataclasses import dataclass


@dataclass
class Move:
    dx: float
    dy: float
    duration: int
