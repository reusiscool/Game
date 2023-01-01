import pygame

from loot.baseLoot import BaseLoot
from player import Player


class HealthLoot(BaseLoot):
    def __init__(self, pos, amount):
        surf = pygame.Surface((10, 10))
        surf.fill('red')
        super().__init__(pos, [surf])
        self.amount = amount

    def add_amount(self, obj: Player, board):
        obj.add_health(self.amount)
