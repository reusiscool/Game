import pygame
from abc import ABC, abstractmethod

from mixer import Mixer
from utils.converters import mum_convert
from player import Player


class BaseLoot(ABC):
    def __init__(self, pos, image_list: list[pygame.Surface]):
        self.image_index = 0
        self.x, self.y = pos
        self.hitbox_size = 15
        self.image_list = image_list

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.hitbox_size, self.hitbox_size)

    @property
    def pos(self):
        return self.x, self.y

    @abstractmethod
    def add_amount(self, obj, board):
        pass

    def tile_pos(self, tile_size):
        return self.x // tile_size, self.y // tile_size

    def update(self, board):
        for obj in board.get_objects(self.pos, self.hitbox_size * 3):
            if self.rect.colliderect(obj.rect) and isinstance(obj, Player):
                board.pop_loot(self)
                Mixer().on_pick()
                self.add_amount(obj, board)

    def render(self, surf, camera_x, camera_y):
        self.image_index += 1
        self.image_index %= len(self.image_list)
        img = self.image_list[self.image_index]
        x, y = mum_convert(*self.pos)
        off_x = img.get_width() // 2
        off_y = img.get_height()
        surf.blit(img, (x - camera_x - off_x, y - camera_y - off_y + self.hitbox_size // 2))
