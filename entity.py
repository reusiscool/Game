from dataclasses import dataclass
from math import ceil
from typing import Tuple
from enum import Enum
import pygame

from abc import ABC, abstractmethod
from utils.converters import mum_convert
from utils.customFont import single_font
from utils.move import Move
from effects import Effect, EffectContainer


@dataclass(slots=True)
class EntityStats:
    """square: (x0, y0, width)"""
    square: tuple
    speed: int
    health: int
    max_health: int

    def heal(self, amount):
        if self.health >= self.max_health:
            return
        self.health = min(self.max_health, self.health + amount)


class Team(Enum):
    Enemy = 1
    Player = 2
    Null = 3


class Entity(ABC):
    def __init__(self, image_list: list[pygame.Surface], ents: EntityStats):
        self.x, self.y, self.hitbox_size = ents.square
        self.stats = ents
        self.image_list = image_list
        self.image_index = 0
        self.move_q: list[Move] = []
        self.looking_direction = (0, 0)
        self.damage_time = 0
        self.damage_img = None
        self.collided = False
        self.effects: list[EffectContainer] = []

    @property
    def rect(self):
        return pygame.rect.Rect(self.x, self.y, self.hitbox_size, self.hitbox_size)

    @property
    @abstractmethod
    def team(self):
        return ...

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

    def _get_effect(self, effect):
        mult = 0
        for i in self.effects:
            if i.effect == effect:
                mult += i.stats
        return mult / 100

    @property
    def _receive_damage_multiplier(self):
        return 1

    @property
    def _movement_multiplier(self):
        return max(0, 1 - self._get_effect(Effect.Slowness) + self._get_effect(Effect.Swiftness))

    def damage(self, amount):
        if amount < 0:
            return
        amount = ceil(amount * self._receive_damage_multiplier)
        font = single_font('large_font')
        self.damage_img = font.render(str(amount))
        self.stats.health = max(0, self.stats.health - amount)

    @property
    def pos(self) -> Tuple[float, float]:
        return self.x, self.y

    def tile_pos(self, tile_size):
        return int(self.x // tile_size), int(self.y // tile_size)

    def calc_movement(self):
        dx = 0
        dy = 0
        for mov in self.move_q:
            if mov.own_speed:
                dx += mov.dx * self.stats.speed * self._movement_multiplier
                dy += mov.dy * self.stats.speed * self._movement_multiplier
                continue
            dx += mov.dx
            dy += mov.dy
        for i in self.move_q:
            i.update()
        self.move_q = [i for i in self.move_q if i.duration > 0]
        return dx, dy

    def update_effects(self):
        for i in self.effects:
            i.update()
        self.effects = [i for i in self.effects if i.time_left >= 0]

    def update(self, board):
        board.pop_entity(self)
        self.collided = False
        dx, dy = self.calc_movement()
        ls = board.get_objects(self.pos, 100)
        self._move_x(dx, ls)
        self._move_y(dy, ls)
        if self.stats.health > 0:
            board.add_entity(self)
        self.update_effects()

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
        if self.damage_img:
            surf.blit(self.damage_img, (x - camera_x - off_x,
                                        y - camera_y - off_y + self.hitbox_size // 2))
            self.damage_time += 1
            if self.damage_time > 20:
                self.damage_img = None
                self.damage_time = 0

    def nudge(self):
        self.move_q.append(Move(0.001, 0.001, 1))
