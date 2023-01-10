import pygame

from loot.baseLoot import BaseLoot
from player import Player
from utils.infoDisplay import generate_description
from utils.savingConst import SavingConstants


class HealthLoot(BaseLoot):
    def __init__(self, pos, amount=None):
        surf = pygame.Surface((10, 10))
        surf.fill('red')
        super().__init__(pos, [surf])
        self.amount = amount if amount is not None else 10

    @property
    def desc(self):
        return generate_description('large_font', {'Heal amount': self.amount}, "Health loot")

    def add_amount(self, obj: Player, board):
        obj.add_health(self.amount)

    def serialize(self):
        return SavingConstants().get_const(HealthLoot), self.pos, self.amount
