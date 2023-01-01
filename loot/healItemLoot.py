import pygame

from loot.baseLoot import BaseLoot
from items.healItem import HealItem


class HealItemLoot(BaseLoot):
    def __init__(self, pos, amount):
        s = pygame.Surface((10, 10))
        s.fill('purple')
        super().__init__(pos, [s])
        self.item = HealItem(amount)

    def add_amount(self, obj, board):
        if obj.inventory.add_item(self.item):
            return
        board.add_loot(self)