from math import dist, cos, radians
from dataclasses import dataclass
import pygame

from baseWeapon import BaseWeapon
from converters import mum_convert
from entity import Entity
from move import Move
from utils import vector_angle, normalize, rotate


@dataclass(frozen=True)
class SwordStats:
    damage: int
    range_: int
    angle: int
    cooldown: int
    knockback: int


class Sword(BaseWeapon):

    def __init__(self, image_list: list[pygame.Surface], owner: Entity, sword_stats: SwordStats):
        super().__init__(image_list, owner)
        self.angle_range = sword_stats.angle
        self.damage = sword_stats.damage
        self.cosa = cos(radians(self.angle_range))
        self.range_ = sword_stats.range_
        self.cooldown = sword_stats.cooldown
        self.knockback = sword_stats.knockback

    def get_stats(self):
        return SwordStats(self.damage, self.range_, self.angle_range, self.cooldown, self.knockback)

    def attack(self, board):
        if self.current_cooldown:
            return
        sx, sy = self.owner.pos
        ls = board.get_entities(self.owner.pos, self.range_)
        for obj in ls:
            if obj == self.owner:
                continue
            if dist(obj.pos, self.owner.pos) <= self.range_ and \
                    vector_angle((obj.x - self.owner.x, obj.y - self.owner.y), self.owner.looking_direction) >= self.cosa:
                obj.damage(self.damage)
                m1 = Move(obj.x - sx, obj.y - sy, 7, normalize=True)
                m1.amplify(self.knockback // 7)
                obj.move_move(Move(obj.x - sx, obj.y - sy, 10, own_speed=True, normalize=True))
                obj.move_move(m1)
        self.current_cooldown = self.cooldown
        self.image_index = min(len(self.image_list) - 1, 1)

    def render(self, surf, camera_x, camera_y):
        self.draw_attack_lines(surf, camera_x, camera_y)
        img = self.image_list[self.image_index]
        x, y = mum_convert(*self.owner.pos)
        off_x = img.get_width() // 2 + self.weapon_x_offset
        if not self.owner.looking_direction[0] < self.owner.looking_direction[1]:
            img = pygame.transform.flip(img, True, False)
            off_x -= self.weapon_x_offset * 2
        off_y = img.get_height() + self.weapon_y_offset
        surf.blit(img, (x - camera_x - off_x, y - camera_y - off_y))
        if self.image_index:
            self.image_index += 1
            self.image_index %= len(self.image_list)

    def draw_attack_lines(self, surf, cx, cy):
        x, y = normalize(*self.owner.looking_direction)
        px, py = mum_convert(*self.owner.pos)
        # nx, ny = self.draw_line((x, y), self.range_)
        # pygame.draw.line(surf, 'orange', (px - cx, py - cy), (nx - cx, ny - cy), 2)
        for line in rotate((x, y), self.angle_range - 10):
            nx, ny = self.draw_line(line, self.range_)
            pygame.draw.line(surf, 'orange', (px - cx, py - cy), (nx - cx, ny - cy), 5)
