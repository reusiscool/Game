import pygame

from converters import mum_convert
from entity import Entity


class BaseProjectile:
    def __init__(self, pos, hitbox_size, image_list: list[pygame.Surface], lifetime, owner, vlist, damage):
        self.image_list = image_list
        self.hitbox_size = hitbox_size
        self.x, self.y = pos
        self.owner = owner
        self.lifetime = lifetime
        self.time = 0
        self.vx, self.vy = vlist
        self.damage = damage
        self.image_index = 0

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.hitbox_size, self.hitbox_size)

    @property
    def pos(self):
        return self.x, self.y

    def _move_y(self, dy, map_):
        if not dy:
            return
        self.y += dy
        rect = self.rect
        for obj in map_:
            if obj == self.owner:
                continue
            if rect.colliderect(obj.rect):
                if isinstance(obj, Entity):
                    obj.damage(self.damage)
                self.time = self.lifetime + 1

    def _move_x(self, dx, map_):
        if not dx:
            return
        self.x += dx
        rect = self.rect
        for obj in map_:
            if obj == self.owner:
                continue
            if rect.colliderect(obj.rect):
                if isinstance(obj, Entity):
                    obj.damage(self.damage)
                self.time = self.lifetime + 1

    def update(self, board):
        ls = board.get_objects(self.pos, 100)
        self._move_x(self.vx, ls)
        self._move_y(self.vy, ls)
        if self.time > self.lifetime:
            board.pop_projectile(self)
        self.time += 1

    def render(self, surf: pygame.Surface, camera_x, camera_y):
        self.image_index += 1
        self.image_index %= len(self.image_list)
        img = self.image_list[self.image_index]
        x, y = mum_convert(*self.pos)
        off_x = img.get_width() // 2
        off_y = img.get_height()
        surf.blit(img, (x - camera_x - off_x, y - camera_y - off_y + self.hitbox_size // 2))
