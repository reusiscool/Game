import pygame

from loot.baseLoot import BaseLoot


class SkillPointLoot(BaseLoot):
    def __init__(self, pos):
        image_list = [pygame.Surface((10, 10))]
        image_list[0].fill('white')
        super().__init__(pos, image_list)

    def add_amount(self, obj, board):
        obj.stats.skill_points += 1
