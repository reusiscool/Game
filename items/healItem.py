import pygame

from items.baseItem import BaseItem
from utils.infoDisplay import generate_description
from items.itemConst import ItemConstants


class HealItem(BaseItem):
    def __init__(self, heal_amount):
        surf = pygame.Surface((20, 20))
        surf.fill('red')
        desc = generate_description('large_font', {'Heals': heal_amount}, 'Heal item')
        super().__init__(surf, desc)
        self.heal_amount = heal_amount

    def use(self, owner):
        owner.add_health(self.heal_amount)
        return True

    def serialize(self):
        return ItemConstants().const[HealItem], self.heal_amount
