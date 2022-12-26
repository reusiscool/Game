from dataclasses import dataclass
import pygame

from baseEnemy import BaseEnemy, EnemyStats


class ShootingEnemy(BaseEnemy):
    def __init__(self, pos, hitbox_size, image_list: list[pygame.Surface], es: EnemyStats):
        super().__init__(pos, hitbox_size, image_list, es)

    def attack(self):
        pass



