import pygame

from loot.baseLoot import BaseLoot
from utils.infoDisplay import generate_description
from utils.savingConst import SavingConstants


class SkillPointLoot(BaseLoot):
    def __init__(self, pos):
        image_list = [pygame.Surface((10, 10))]
        image_list[0].fill('white')
        super().__init__(pos, image_list)

    def add_amount(self, obj, board):
        obj.stats.skill_points += 1

    def serialize(self):
        return SavingConstants().get_const(SkillPointLoot), self.pos

    @property
    def desc(self):
        return generate_description('large_font', ['Adds one skill point.'], "Skill point")

    @classmethod
    def read(cls, line):
        pos = eval(line[1])
        return cls(pos)
