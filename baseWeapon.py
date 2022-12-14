from abc import ABC, abstractmethod
import pygame

from entity import Entity


class BaseWeapon(ABC):
    weapon_x_offset = 13
    weapon_y_offset = 20

    def __init__(self, image_list: list[pygame.Surface], owner: Entity):
        self.owner = owner
        self.image_list = image_list
        self.image_index = 0
        self.current_cooldown = 0
        self.cooldown = None

    @abstractmethod
    def attack(self, board):
        pass

    def update(self):
        self.current_cooldown = max(0, self.current_cooldown - 1)

    @abstractmethod
    def render(self, surf, camera_x, camera_y):
        pass
