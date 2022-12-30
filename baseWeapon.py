from abc import ABC, abstractmethod
import pygame

from converters import mum_convert
from entity import Entity


class BaseWeapon(ABC):
    weapon_x_offset = 13
    weapon_y_offset = 20

    def __init__(self, image_list: list[pygame.Surface], owner: Entity):
        self.owner = owner
        self.image_list = image_list
        self.image_index = 0
        self.current_cooldown = 0

    @abstractmethod
    def attack(self, board):
        pass

    def update(self):
        self.current_cooldown = max(0, self.current_cooldown - 1)

    @abstractmethod
    def render(self, surf, camera_x, camera_y):
        pass

    def draw_line(self, norm_pos, distance):
        x, y = norm_pos
        x *= distance
        y *= distance
        x += self.owner.x
        y += self.owner.y
        x, y = mum_convert(x, y)
        return x, y
