import pygame

from loot.baseLoot import BaseLoot
from items.keyItem import KeyItem
from utils.savingConst import SavingConstants
from utils.utils import load_image


class KeyItemLoot(BaseLoot):
    def __init__(self, pos, id_):
        s = load_image('key', 'key_item.png', color_key='white')
        # s = pygame.transform.scale(s, (20, 20))
        super().__init__(pos, [s])
        self.item = KeyItem(id_)

    def add_amount(self, obj, board):
        if obj.inventory.add_item(self.item):
            return
        board.add_noncollider(self)

    def serialize(self):
        return SavingConstants().get_const(type(self)),\
               (int(self.x), int(self.y)), self.item.lock_id
