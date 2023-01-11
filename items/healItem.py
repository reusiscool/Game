import pygame

from items.baseItem import BaseItem
from utils.infoDisplay import generate_description
from utils.savingConst import SavingConstants


class HealItem(BaseItem):
    def __init__(self, heal_amount=None):
        surf = pygame.Surface((20, 20))
        surf.fill('red')
        self.heal_amount = heal_amount if heal_amount is not None else 10
        desc = generate_description('large_font', {'Heals': heal_amount}, 'Heal item')
        super().__init__(surf, desc)

    def use(self, owner):
        owner.add_health(self.heal_amount)
        return True

    def serialize(self):
        return SavingConstants().get_const(HealItem), self.heal_amount
