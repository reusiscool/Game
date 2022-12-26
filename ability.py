import pygame

from baseWeapon import BaseWeapon
from entity import Entity
from baseProjectile import BaseProjectile
from utils import normalize


class Ability(BaseWeapon):
    def __init__(self, image_list: list[pygame.Surface], owner: Entity):
        super().__init__(image_list, owner)
        self.cooldown = 10
        self.cost = 10

    def attack(self, board):
        if self.current_cooldown or self.owner.mana < self.cost:
            return
        self.owner.mana -= self.cost
        self.current_cooldown = self.cooldown
        bsurf = pygame.Surface((10, 10))
        bsurf.fill('red')
        vx, vy = normalize(*self.owner.looking_direction)
        vx *= 8
        vy *= 8
        b = BaseProjectile(self.owner.pos, 10, [bsurf], 420, self.owner, (vx, vy), 20)
        board.add_projectile(b)

    def render(self, surf, camera_x, camera_y):
        pass
