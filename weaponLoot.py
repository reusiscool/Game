import pygame

from basePickable import BasePickable
from baseWeapon import BaseWeapon
from customFont import single_font


class WeaponLoot(BasePickable):
    def __init__(self, pos, image_list, weapon: BaseWeapon):
        super().__init__(pos, image_list)
        self.weapon = weapon
        self.hitbox_size = 100
        self.font = single_font('large_font')
        self.desc = pygame.Surface((80, 150))
        self.generate_description()

    def add_amount(self, obj):
        obj.weapon_list[obj.weapon_index] = self.weapon

    def generate_description(self):
        self.font.render(self.desc, 'Weapon', (0, 0))
        d = self.weapon.stats.__dict__
        for i, val in enumerate(d):
            self.font.render(self.desc, f'{val}: {d[val]}', (1, (i + 1) * (self.font.height + 1)))

    def render(self, surf: pygame.Surface, camera_x, camera_y):
        super().render(surf, camera_x, camera_y)
        if self.highlighted:
            surf.blit(self.desc, (surf.get_width() - self.desc.get_width(), 0))

