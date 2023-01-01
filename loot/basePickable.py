from abc import ABC
import pygame

from loot.baseLoot import BaseLoot
from utils.converters import mum_convert
from player import Player


class BasePickable(BaseLoot, ABC):
    def __init__(self, pos, image_list):
        super().__init__(pos, image_list)
        self.highlighted = False

    def update(self, board):
        for obj in board.get_entities(self.pos, self.hitbox_size * 3):
            if self.rect.colliderect(obj.rect) and isinstance(obj, Player):
                if obj.is_interacting:
                    board.pop_loot(self)
                    self.add_amount(obj, board)
                else:
                    self.highlighted = True
                break
        else:
            self.highlighted = False

    def render(self, surf, camera_x, camera_y):
        self.image_index += 1
        self.image_index %= len(self.image_list)
        img = self.image_list[self.image_index]
        if self.highlighted:
            new_img = pygame.Surface(img.get_size())
            new_img.fill('white')
            s = pygame.Surface(img.get_size())
            s.fill('white')
            s.set_alpha(100)
            new_img.blit(img, (0, 0))
            new_img.set_colorkey('white')
            new_img.blit(s, (0, 0))
            img = new_img
        x, y = mum_convert(*self.pos)
        off_x = img.get_width() // 2
        off_y = img.get_height()
        surf.blit(img, (x - camera_x - off_x, y - camera_y - off_y + self.hitbox_size // 2))
