from abc import ABC, abstractmethod
import pygame

from utils.converters import mum_convert


class BaseWeapon(ABC):
    weapon_x_offset = 13
    weapon_y_offset = 20

    def __init__(self, image_list: list[pygame.Surface]):
        self.image_list = image_list
        self.image_index = 0
        self.current_cooldown = 0

    @property
    @abstractmethod
    def desc(self):
        pass

    @abstractmethod
    def attack(self, board, owner):
        pass

    def update(self):
        self.current_cooldown = max(0, self.current_cooldown - 1)

    @abstractmethod
    def render(self, surf, camera_x, camera_y, owner):
        pass

    def draw_line(self, norm_pos, distance, owner):
        x, y = norm_pos
        x *= distance
        y *= distance
        x += owner.x
        y += owner.y
        x, y = mum_convert(x, y)
        return x, y

    @abstractmethod
    def serialize(self):
        pass
