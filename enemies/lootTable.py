from random import randint

from loot.moneyLoot import MoneyLoot
from loot.manaLoot import ManaLoot
from loot.healthLoot import HealthLoot
from loot.healItemLoot import HealItemLoot


class LootTable:
    def __init__(self, drops):
        """List[Tuple[Drop, Chance in per cents]]"""
        self.drops = drops

    def roll(self):
        a = randint(0, 100)
        for drop, chance in self.drops:
            a -= chance
            if a <= 0:
                return drop
        return lambda x: None


class EnemyLootTable(LootTable):
    def __init__(self):
        drops = [(MoneyLoot, 15),
                 (ManaLoot, 30),
                 (HealthLoot, 10),
                 (HealItemLoot, 5)]
        super().__init__(drops)
