import pygame

from loot.baseLoot import BaseLoot
from items.keyItem import KeyItem


class KeyItemLoot(BaseLoot):
    def __init__(self, pos, id_):
        s = pygame.Surface((10, 10))
        s.fill('gold')
        super().__init__(pos, [s])
        self.item = KeyItem(id_)

    def add_amount(self, obj, board):
        if obj.inventory.add_item(self.item):
            return
        board.add_noncollider(self)
