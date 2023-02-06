import pygame

from interactables.baseShop import BaseShop
from utils.infoDisplay import generate_description
from utils.savingConst import SavingConstants


class Shop(BaseShop):
    def __init__(self, pos, rarity: int, level=0, goods=None):
        """rarity is an integer from 0 to 3 inclusive"""
        surf = pygame.Surface((50, 50))
        surf.fill('brown')
        image_list = [surf]
        super().__init__(pos, rarity, image_list, level, goods)

    def _list_of_goods(self, rarity, level):
        return SavingConstants().get_shop_items(rarity, level)

    def get_desc(self):
        return generate_description('large_font', {'Rarity': self.rarity}, 'Shop')

    @classmethod
    def read(cls, line):
        pos, rarity, goods = BaseShop._shop_info(line)
        return cls(pos, rarity, goods=goods)
