from dataclasses import dataclass
import pygame

from utils.converters import mum_convert


@dataclass
class TrapStats:
    damage: int
    cooldown: int
    rect: pygame.Rect
    time_up: int = None

    def __post_init__(self):
        if self.time_up is None:
            self.time_up = self.cooldown


class Trap:
    def __init__(self, ts: TrapStats, image_list: list[pygame.Surface]):
        self.image_list = image_list
        self.ts = ts
        self.time = 0

    def check_collision(self, board):
        for obj in board.get_entities(self.ts.rect.center, self.ts.rect.width * 3):
            if self.ts.rect.colliderect(obj.rect):
                obj.damage(self.ts.damage)
                self.time = 0
                return

    @property
    def pos(self):
        return self.ts.rect.x, self.ts.rect.y

    def tile_pos(self, tile_size):
        return self.ts.rect.x // tile_size, self.ts.rect.y // tile_size

    def update(self, board):
        if self.time > self.ts.cooldown:
            self.check_collision(board)
        self.time += 1
        if self.time > self.ts.cooldown + self.ts.time_up:
            self.time = 0

    def render(self, surf, camera_x, camera_y):
        ind = max(0, self.time - self.ts.cooldown)
        ind = min(len(self.image_list) - 1, ind)
        img = self.image_list[ind]
        x, y = mum_convert(self.ts.rect.x, self.ts.rect.y)
        surf.blit(img, (x - camera_x - img.get_width() // 2, y - camera_y))
