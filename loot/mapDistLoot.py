import pygame

from loot.baseLoot import BaseLoot
from utils.infoDisplay import generate_description
from utils.savingConst import SavingConstants


class MapDistLoot(BaseLoot):
    def __init__(self, pos):
        s = pygame.Surface((10, 10))
        s.fill('green')
        super().__init__(pos, [s])

    @property
    def desc(self):
        return generate_description('large_font', ['Extends map reveal distance'], "Map read item")

    def add_amount(self, obj, board):
        obj.stats.reveal_distance += 1

    def serialize(self):
        return SavingConstants().get_const(MapDistLoot), self.pos

    @classmethod
    def read(cls, line):
        pos = eval(line[1])
        return cls(pos)
