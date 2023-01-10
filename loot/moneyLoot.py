import os
import pygame
from random import randint

from loot.baseLoot import BaseLoot
from utils.savingConst import SavingConstants


class MoneyLoot(BaseLoot):
    def __init__(self, pos, amount=None):
        surf = pygame.Surface((10, 10))
        surf.fill((255, 255, 100))
        image_list = [surf]
        super().__init__(pos, image_list)
        self.amount = self._get_amount() if amount is None else amount

    def _get_amount(self):
        with open(os.path.join('levels', 'GameState.txt')) as f:
            level = int(f.readline())
        g = SavingConstants().gold_drop[level - 1] + randint(0, 4) - 2
        return g

    def add_amount(self, obj, board):
        obj.stats.gold += self.amount
