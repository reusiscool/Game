import pygame
from abc import ABC

from converters import mum_convert
from move import Move
from states import Stat


class Entity(ABC):
    def __init__(self, pos, hitbox_size, image_list: list[pygame.Surface], speed=2, health=0, max_health=0):
        self.x = pos[0]
        self.y = pos[1]
        self.hitbox_size = hitbox_size
        self.image_list = image_list
        self.image_index = 0
        self.move_q: list[Move] = []
        self.stats = {Stat.Health: health, Stat.MaxHealth: max_health, Stat.Speed: speed}
        self.looking_direction = (0, 0)
        self.collided = False

    @property
    def rect(self):
        return pygame.rect.Rect(self.x, self.y, self.hitbox_size, self.hitbox_size)

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
                self.collided = True
                if dx > 0:
                    rect.right = r.left
                else:
                    rect.left = r.right
                self.x = rect.x

    def damage(self, amount):
        if amount < 0:
            return
        self.stats[Stat.Health] = max(0, self.stats[Stat.Health] - amount)

    def _move_y(self, dy, map_):
        if not dy:
            return
        self.y += dy
        rect = self.rect
        for obj in map_:
            r = obj.rect
            if rect.colliderect(r):
                self.collided = True
                if dy > 0:
                    rect.bottom = r.top
                else:
                    rect.top = r.bottom
                self.y = rect.y

    @property
    def pos(self):
        return self.x, self.y

    def tile_pos(self, tile_size):
        return self.x // tile_size, self.y // tile_size

    def calc_movement(self):
        dx = 0
        dy = 0
        for mov in self.move_q:
            if mov.own_speed:
                dx += mov.dx * self.stats[Stat.Speed]
                dy += mov.dy * self.stats[Stat.Speed]
                continue
            dx += mov.dx
            dy += mov.dy
        for i in self.move_q:
            i.update()
        self.move_q = [i for i in self.move_q if i.duration > 0]
        return dx, dy

    def update(self, board):
        board.pop_entity(self)
        self.collided = False
        dx, dy = self.calc_movement()
        ls = board.get_objects(self.pos, 100)
        self._move_x(dx, ls)
        self._move_y(dy, ls)
        if self.stats[Stat.Health] > 0:
            board.add_entity(self)

    def render(self, surf: pygame.Surface, camera_x, camera_y):
        self.image_index += 1
        self.image_index %= len(self.image_list)
        img = self.image_list[self.image_index]
        lx, ly = self.looking_direction
        if ly > lx:
            img = pygame.transform.flip(img, True, False)
        x, y = mum_convert(*self.pos)
        off_x = img.get_width() // 2
        off_y = img.get_height()
        surf.blit(img, (x - camera_x - off_x, y - camera_y - off_y + self.hitbox_size // 2))

    def nudge(self):
        self.move_q.append(Move(0.001, 0.001, 1))
