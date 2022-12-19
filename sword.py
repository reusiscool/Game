import pygame
from math import dist, cos, radians

from baseWeapon import BaseWeapon
from converters import mum_convert
from entity import Entity
from move import Move
from utils import vector_angle, normalize, rotate


class Sword(BaseWeapon):
    angle_range = 45
    cosa = cos(angle_range)

    def __init__(self, image_list: list[pygame.Surface], owner: Entity):
        super().__init__(image_list, owner)
        self.range_ = 100
        self.cooldown = 10

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
                obj.damage(20)
                obj.move_move(Move(obj.x - sx, obj.y - sy, 10, own_speed=True))
                obj.move_move(Move(obj.x - sx, obj.y - sy, 7, own_speed=True))
                obj.move_move(Move(obj.x - sx, obj.y - sy, 4, own_speed=True))
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
