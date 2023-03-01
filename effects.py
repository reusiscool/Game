from dataclasses import dataclass, field
from enum import Enum


class Effect(Enum):
    Slowness = 0
    Swiftness = 1
    Strength = 2
    Crit = 3

    def get_stats(self, lvl):
        if self == Effect.Slowness:
            return [5, 10, 15, 20][lvl - 1]
        if self == Effect.Swiftness:
            return [5, 10, 15, 20][lvl - 1]
        if self == Effect.Crit:
            return [5, 10, 15, 20][lvl - 1]


@dataclass(slots=True)
class EffectContainer:
    effect: Effect
    level: int
    time_left: int
    _stats: any = field(default=None)

    @property
    def stats(self):
        if self._stats is None:
            self._stats = self._get_stats()
        return self._stats

    def _get_stats(self):
        return self.effect.get_stats(self.level)

    def update(self):
        self.time_left -= 1
