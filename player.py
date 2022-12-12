import pygame
import converters
from entity import Entity
from move import Move
from utils import normalize


class Player(Entity):
    def __init__(self, pos, hitbox_size, image, speed):
        super().__init__(pos, hitbox_size, image, speed)
        self.dash_cooldown = 60
        self.dash_current_cooldown = 0
        self.dash_speed = 3

    def render(self, surf: pygame.Surface, camera_x, camera_y):
        x, y = converters.mum_convert(*self.pos)
        off_x = self.image.get_width() // 2
        off_y = self.image.get_height()
        surf.blit(self.image, (x - camera_x - off_x, y - camera_y - off_y + self.hitbox_size // 2))

    def update(self, board):
        super().update(board)
        self.dash_current_cooldown = max(0, self.dash_current_cooldown - 1)

    def dash(self, dx, dy):
        dx, dy = normalize(dx, dy)
        if self.dash_current_cooldown:
            return
        self.dash_current_cooldown = self.dash_cooldown
        self.move_q.append(Move(dx * self.dash_speed, dy * self.dash_speed, 10))
        self.move_q.append(Move(dx * self.dash_speed, dy * self.dash_speed, 7))
        self.move_q.append(Move(dx * self.dash_speed, dy * self.dash_speed, 4))
        self.move_q.append(Move(dx * self.dash_speed, dy * self.dash_speed, 2))
