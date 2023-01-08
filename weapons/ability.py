import pygame

from weapons.baseWeapon import BaseWeapon
from weapons.baseProjectile import BaseProjectile
from utils.utils import normalize, load_image


class Ability(BaseWeapon):
    def __init__(self):
        image_list = [load_image('sword', 'sword.png', color_key='white')]
        super().__init__(image_list)
        self.cooldown = 10
        self.cost = 10

    def attack(self, board, owner):
        if self.current_cooldown or owner.stats.mana < self.cost:
            return
        owner.stats.mana -= self.cost
        self.current_cooldown = self.cooldown
        bsurf = pygame.Surface((10, 10))
        bsurf.fill('red')
        vx, vy = normalize(*owner.looking_direction)
        vx *= 8
        vy *= 8
        b = BaseProjectile(owner.pos, 10, [bsurf], 420, owner, (vx, vy), 20)
        board.add_projectile(b)

    def render(self, *args):
        pass

    def serialize(self):
        return self.cooldown, self.cost
