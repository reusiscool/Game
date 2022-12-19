from states import return_pic, Stat
from baseLoot import BaseLoot
from player import Player


class ManaLoot(BaseLoot):
    def __init__(self, pos, amount):
        super().__init__(pos, return_pic(Stat.Mana))
        self.amount = amount

    def add_amount(self, obj: Player):
        obj.stats[Stat.Mana] = min(obj.stats[Stat.Mana] + self.amount, obj.stats[Stat.MaxMana])
