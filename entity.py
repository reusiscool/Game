import pygame
from abc import ABC

from converters import mum_convert
from move import Move
from utils import normalize


class Entity(ABC):
    def __init__(self, pos, hitbox_size, image_list: list[pygame.Surface], speed=2, health=0, max_health=0):
        self.max_health = max_health
        self.current_health = health
        self.x = pos[0]
        self.y = pos[1]
        self.hitbox_size = hitbox_size
        self.image_list = image_list
        self.image_index = 0
        self.move_q: list[Move] = []
        self.speed = speed
        self.is_flipped = False
        self.looking_direction = (0, 0)

    @property
    def rect(self):
        return pygame.rect.Rect(self.x, self.y, self.hitbox_size, self.hitbox_size)

    def move_coords(self, x, y, dur=1, own_speed=False):
        self.move_q.append(Move(x, y, dur, own_speed=own_speed))

    def move_move(self, move: Move):
        self.move_q.append(move)

    def _move_x(self, dx, map_):
        if not dx:
            return
        self.x += dx
        rect = self.rect
        for obj in map_:
            r = obj.rect
            if rect.colliderect(r):
                if dx > 0:
                    rect.right = r.left
                else:
                    rect.left = r.right
                self.x = rect.x

    def damage(self, amount):
        if amount < 0:
            return
        self.current_health = max(0, self.current_health - amount)

    def _move_y(self, dy, map_):
        if not dy:
            return
        self.y += dy
        rect = self.rect
        for obj in map_:
            r = obj.rect
            if rect.colliderect(r):
                if dy > 0:
                    rect.bottom = r.top
                else:
                    rect.top = r.bottom
                self.y = rect.y

    @property
    def pos(self):
        return self.x, self.y

    def calc_movement(self):
        dx = 0
        dy = 0
        for mov in self.move_q:
            if mov.own_speed:
                sx, sy = normalize(*mov.pos)
                dx += sx * self.speed
                dy += sy * self.speed
                continue
            dx += mov.dx
            dy += mov.dy
        for i in self.move_q:
            i.update()
        self.move_q = [i for i in self.move_q if i.duration > 0]
        return dx, dy

    def update(self, board):
        board.pop_entity(self)
        dx, dy = self.calc_movement()
        if dx - dy > 0:
            self.is_flipped = False
        elif dx - dy < 0:
            self.is_flipped = True
        ls = board.get_objects(self.pos, 100)
        self._move_x(dx, ls)
        self._move_y(dy, ls)
        if self.current_health > 0:
            board.add_entity(self)

    def render(self, surf: pygame.Surface, camera_x, camera_y):
        self.image_index += 1
        self.image_index %= len(self.image_list)
        img = self.image_list[self.image_index]
        if self.is_flipped:
            img = pygame.transform.flip(img, True, False)
        x, y = mum_convert(*self.pos)
        off_x = img.get_width() // 2
        off_y = img.get_height()
        surf.blit(img, (x - camera_x - off_x, y - camera_y - off_y + self.hitbox_size // 2))
