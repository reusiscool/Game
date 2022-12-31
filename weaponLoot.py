import pygame

from basePickable import BasePickable
from baseWeapon import BaseWeapon
from infoDisplay import generate_description


class WeaponLoot(BasePickable):
    def __init__(self, pos, image_list, weapon: BaseWeapon):
        super().__init__(pos, image_list)
        self.weapon = weapon
        self.hitbox_size = 100
        self.desc = pygame.Surface((80, 150))
        self.generate_description()

    def add_amount(self, obj):
        obj.weapon_list[obj.weapon_index] = self.weapon

    def generate_description(self):
        self.desc = generate_description('large_font', self.weapon.stats.__dict__, 'Weapon')

    def render(self, surf: pygame.Surface, camera_x, camera_y):
        super().render(surf, camera_x, camera_y)
        if self.highlighted:
            surf.blit(self.desc, (surf.get_width() - self.desc.get_width(), 0))

