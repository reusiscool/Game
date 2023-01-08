import pygame

from interactables.baseInteractable import BaseInteractable
from weapons.baseWeapon import BaseWeapon
from utils.infoDisplay import generate_description
from utils.savingConst import SavingConstants


class WeaponLoot(BaseInteractable):
    def __init__(self, pos, weapon: BaseWeapon):
        self.weapon = weapon
        image_list = weapon.image_list
        super().__init__(pos, image_list)
        self.hitbox_size = 100

    def interact(self, obj, board):
        board.pop_loot(self)
        obj.weapon_list[obj.weapon_index] = self.weapon

    def get_desc(self):
        return generate_description('large_font', self.weapon.stats.__dict__, 'Weapon')

    def render(self, surf: pygame.Surface, camera_x, camera_y):
        super().render(surf, camera_x, camera_y)

    def serialize(self):
        return SavingConstants().get_const(type(self)), *self.weapon.serialize(),\
               tuple(int(i) for i in self.pos)
