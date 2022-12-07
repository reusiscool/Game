import pygame
from abc import ABC, abstractmethod
from move import Move


class Entity(ABC):
    def __init__(self, pos, hitbox_size, image):
        self.x = pos[0]
        self.y = pos[1]
        self.hitbox_size = hitbox_size
        self.image = image
        self.move_q: list[Move] = []

    @property
    def rect(self):
        return pygame.rect.Rect(self.x, self.y, self.hitbox_size, self.hitbox_size)

    def move_coords(self, x, y, dur=1):
        self.move_q.append(Move(x, y, dur))

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
        dx = sum(i.dx for i in self.move_q)
        dy = sum(i.dy for i in self.move_q)
        self.move_q = [Move(i.dx, i.dy, i.duration) for i in self.move_q if i.duration > 1]
        return dx, dy

    def update(self, board):
        board.pop(self)
        dx, dy = self.calc_movement()
        ls = board.get_objects(self.pos, 100)
        self._move_x(dx, ls)
        self._move_y(dy, ls)
        board.add(self)

    @abstractmethod
    def render(self, surf, camera_x, camera_y):
        pass
