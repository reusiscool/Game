from abc import ABC

import pygame

from loot.baseLoot import BaseLoot
from mixer import Mixer
from player import Player


class BaseItemLoot(BaseLoot, ABC):
    def __init__(self, pos, image_list: list[pygame.Surface], item):
        super().__init__(pos, image_list)
        self.item = item
        self.time = 0

    def add_amount(self, obj, board):
        pass

    def update(self, board):
        for obj in board.get_objects(self.pos, self.hitbox_size * 3):
            if self.rect.colliderect(obj.rect) and isinstance(obj, Player):
                if self.time > 0:
                    self.time -= 1
                    return
                if not obj.inventory.add_item(self.item):
                    self.time = 30
                    Mixer().on_fail()
                    return
                board.pop_loot(self)
                Mixer().on_pick()
