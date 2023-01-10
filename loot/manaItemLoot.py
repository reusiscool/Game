import pygame

from items.manaItem import ManaItem
from loot.baseLoot import BaseLoot
from utils.savingConst import SavingConstants


class ManaItemLoot(BaseLoot):
    def __init__(self, pos, amount=None):
        s = pygame.Surface((10, 10))
        s.fill('purple')
        super().__init__(pos, [s])
        self.item = ManaItem(amount)

    @property
    def desc(self):
        return self.item.description

    def add_amount(self, obj, board):
        if obj.inventory.add_item(self.item):
            return
        board.add_noncollider(self)

    def serialize(self):
        return SavingConstants().get_const(ManaItemLoot), self.pos, self.item.mana_amount
