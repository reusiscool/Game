from dataclasses import dataclass
import pygame

from utils.converters import mum_convert
from utils.savingConst import SavingConstants
from utils.utils import load_image


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
    def __init__(self, ts: TrapStats):
        image_list = [load_image('trap', f'trap{i // 2}.png', color_key='white') for i in range(12)]
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
        if 0 <= (c := (self.ts.cooldown + self.ts.time_up - self.time)) < len(self.image_list):
            ind = c
        else:
            ind = max(0, self.time - self.ts.cooldown)
            ind = min(len(self.image_list) - 1, ind)
        img = self.image_list[ind]
        x, y = mum_convert(self.ts.rect.x, self.ts.rect.y)
        surf.blit(img, (x - camera_x - img.get_width() // 2, y - camera_y))

    def serialize(self):
        return SavingConstants().get_const(type(self)), (int(self.ts.rect.x), int(self.ts.rect.y)), self.ts.damage, self.ts.cooldown, self.ts.time_up

    @classmethod
    def read(cls, line):
        pos = eval(line[1])
        dmg = int(line[2])
        cd = int(line[3])
        up_cd = int(line[4])
        ts = TrapStats(dmg, cd, pygame.Rect(*pos, 100, 100), up_cd)
        return Trap(ts)
