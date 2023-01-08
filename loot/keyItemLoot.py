import pygame

from loot.baseLoot import BaseLoot
from items.keyItem import KeyItem
from utils.savingConst import SavingConstants


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

    def serialize(self):
        return SavingConstants().get_const(type(self)), self.item.lock_id,\
               (int(self.x), int(self.y))
