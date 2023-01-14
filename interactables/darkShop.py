import pygame

from interactables.baseShop import BaseShop
from items.keyItem import KeyItem
from utils.infoDisplay import generate_description
from utils.savingConst import SavingConstants


class DarkShop(BaseShop):
    def __init__(self, pos, rarity: int, locks, level=0, goods=None):
        surf = pygame.Surface((50, 50))
        surf.fill('black')
        image_list = [surf]
        self.locks = locks
        super().__init__(pos, rarity, image_list, level, goods)

    def interact(self, obj, board):
        if not self.locks:
            super().interact(obj, board)
            return
        for i in range(len(obj.inventory.items) - 1, -1, -1):
            item = obj.inventory.items[i]
            if isinstance(item, KeyItem) and item.lock_id in self.locks:
                self.locks.remove(item.lock_id)
                obj.inventory.items.pop(i)
                self.desc = self.get_desc()
                break

    def _list_of_goods(self, rarity, level):
        return SavingConstants().get_dark_shop_items(rarity, level)

    def get_desc(self):
        d = {'Rarity': self.rarity}
        for lock in self.locks:
            d[f'Lock {lock}'] = 'Locked'
        return generate_description('large_font', d, 'DarkShop')

    def serialize(self):
        ls = super().serialize()
        return *ls[:3], tuple(self.locks), *ls[3:]
