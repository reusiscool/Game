from math import dist, cos, radians
from dataclasses import dataclass
import pygame

from weapons.baseWeapon import BaseWeapon
from utils.converters import mum_convert
from utils.move import Move
from utils.utils import vector_angle, normalize, rotate


@dataclass(frozen=True)
class SwordStats:
    damage: int
    range_: int
    angle: int
    cooldown: int
    knockback: int


class Sword(BaseWeapon):
    def __init__(self, image_list: list[pygame.Surface], sword_stats: SwordStats):
        super().__init__(image_list)
        self.stats = sword_stats
        self.image_list = self.image_list * self.stats.cooldown
        self.cosa = cos(radians(sword_stats.angle))

    def get_stats(self):
        return self.stats

    def attack(self, board, owner):
        if self.current_cooldown:
            return
        sx, sy = owner.pos
        ls = board.get_entities(owner.pos, self.stats.range_)
        for obj in ls:
            if obj == owner:
                continue
            if dist(obj.pos, owner.pos) <= self.stats.range_ and \
                    vector_angle((obj.x - owner.x, obj.y - owner.y), owner.looking_direction) >= self.cosa:
                obj.damage(self.stats.damage)
                m1 = Move(obj.x - sx, obj.y - sy, 7, normalize=True)
                m1.amplify(self.stats.knockback // 7)
                obj.move_move(Move(obj.x - sx, obj.y - sy, 10, own_speed=True, normalize=True))
                obj.move_move(m1)
        self.current_cooldown = self.stats.cooldown
        self.image_index = min(len(self.image_list) - 1, 1)

    def render(self, surf, camera_x, camera_y, owner):
        self.draw_attack_lines(surf, camera_x, camera_y, owner)
        img = pygame.transform.rotate(self.image_list[self.image_index], self.image_index)
        x, y = mum_convert(*owner.pos)
        off_x = img.get_width() // 2 + self.weapon_x_offset
        if not owner.looking_direction[0] < owner.looking_direction[1]:
            img = pygame.transform.flip(img, True, False)
            off_x -= self.weapon_x_offset * 2
        off_y = img.get_height() + self.weapon_y_offset
        surf.blit(img, (x - camera_x - off_x, y - camera_y - off_y))
        if self.image_index == 0:
            return
        self.image_index += 1
        self.image_index %= len(self.image_list)

    def draw_attack_lines(self, surf, cx, cy, owner):
        x, y = normalize(*owner.looking_direction)
        px, py = mum_convert(*owner.pos)
        for line in rotate((x, y), self.stats.angle - 10):
            nx, ny = self.draw_line(line, self.stats.range_, owner)
            pygame.draw.line(surf, 'orange', (px - cx, py - cy), (nx - cx, ny - cy), 5)
