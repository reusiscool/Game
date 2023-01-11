from dataclasses import dataclass


@dataclass(slots=True)
class AbilityStats:
    cooldown: int
    cost: int
    damage: int

    def to_dict(self):
        return {'Cooldown': self.cooldown,
                'Cost': self.cost,
                'Damage': self.damage}


class BaseAbility:
    def __init__(self, stats: AbilityStats, image_list):
        self.stats = stats
        self.current_cooldown = 0
        self.image_list = image_list

    def update(self):
        self.current_cooldown = max(0, self.current_cooldown - 1)
