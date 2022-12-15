import pygame

from entity import Entity
from move import Move
from utils import normalize, load_image
from sword import Sword
from converters import mum_convert


class Player(Entity):
    def __init__(self, pos, hitbox_size, image_list, speed, health=0, max_health=0):
        super().__init__(pos, hitbox_size, image_list, speed, health, max_health)
        self.dash_cooldown = 60
        self.dash_current_cooldown = 0
        self.dash_speed = 3
        self.weapon = Sword([load_image('sword', 'sword.png', color_key='white')], self)
        self.try_attack = False
        self.looking_direction = (1, 1)

    def render(self, surf, camera_x, camera_y):
        x, y = normalize(*self.looking_direction)
        x *= self.weapon.range_
        y *= self.weapon.range_
        x += self.x
        y += self.y
        x, y = mum_convert(x, y)
        px, py = mum_convert(*self.pos)
        pygame.draw.line(surf, 'red', (px - camera_x, py - camera_y), (x - camera_x, y - camera_y))
        super().render(surf, camera_x, camera_y)
        self.weapon.render(surf, camera_x, camera_y)

    def attack(self):
        self.try_attack = True

    def update(self, board):
        super().update(board)
        self.dash_current_cooldown = max(0, self.dash_current_cooldown - 1)
        self.weapon.update()
        if self.try_attack:
            self.weapon.attack(board)
            self.try_attack = False

    def move_input(self, x, y):
        self.looking_direction = (x, y)
        self.move_coords(x, y, own_speed=True)

    def dash(self, dx, dy):
        dx, dy = normalize(dx, dy)
        if self.dash_current_cooldown:
            return
        self.dash_current_cooldown = self.dash_cooldown
        self.move_q.append(Move(dx * self.dash_speed, dy * self.dash_speed, 10))
        self.move_q.append(Move(dx * self.dash_speed, dy * self.dash_speed, 7))
        self.move_q.append(Move(dx * self.dash_speed, dy * self.dash_speed, 4))
        self.move_q.append(Move(dx * self.dash_speed, dy * self.dash_speed, 2))
