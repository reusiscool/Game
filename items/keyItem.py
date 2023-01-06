import pygame

from .baseItem import BaseItem
from utils.infoDisplay import generate_description


class KeyItem(BaseItem):
    def __init__(self, lock_id):
        surf = pygame.Surface((20, 20))
        surf.fill('purple')
        desc = generate_description('large_font', {"Opens": lock_id}, 'Key')
        super().__init__(surf, desc)
        self.lock_id = lock_id

    def use(self, owner) -> bool:
        return False
