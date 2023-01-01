import pygame

from loot.baseLoot import BaseLoot
from player import Player


class ManaLoot(BaseLoot):
    def __init__(self, pos, amount):
        surf = pygame.Surface((10, 10))
        surf.fill('blue')
        super().__init__(pos, [surf])
        self.amount = amount

    def add_amount(self, obj: Player, board):
        obj.add_mana(self.amount)
