import pygame

from .baseItem import BaseItem
from utils.infoDisplay import generate_description


class KeyItem(BaseItem):
    def __init__(self, door_id):
        surf = pygame.Surface((20, 20))
        surf.fill('purple')
        desc = generate_description('large_font', {"Opens": door_id}, 'Heal item')
        super().__init__(surf, desc)
        self.door_id = door_id

    def use(self, owner) -> bool:
        return False
