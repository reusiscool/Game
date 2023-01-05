from abc import ABC, abstractmethod
import pygame

from utils.converters import mum_convert
from player import Player


class BaseInteractable(ABC):
    def __init__(self, pos, image_list: list[pygame.Surface]):
        self.image_index = 0
        self.x, self.y = pos
        self.hitbox_size = 10
        self.image_list = image_list
        self.highlighted = False
        self.desc = self.get_desc()

    @abstractmethod
    def get_desc(self):
        pass

    @abstractmethod
    def interact(self, obj, board):
        pass

    def update(self, board):
        for obj in board.get_entities(self.pos, self.hitbox_size * 3):
            if self.rect.colliderect(obj.rect) and isinstance(obj, Player):
                if obj.is_interacting:
                    self.interact(obj, board)
                elif not obj.highlighted:
                    obj.highlighted = True
                    self.highlighted = True
                break
        else:
            self.highlighted = False

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.hitbox_size, self.hitbox_size)

    @property
    def pos(self):
        return self.x, self.y

    def tile_pos(self, tile_size):
        return self.x // tile_size, self.y // tile_size

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
        if self.highlighted:
            surf.blit(self.desc, (surf.get_width() - self.desc.get_width(), 0))
