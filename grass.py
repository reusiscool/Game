from math import cos

import pygame

from converters import mum_convert


class Grass:
    def __init__(self, pos, texture: pygame.Surface):
        self.pos = pos
        self.time = 0
        self.rect = pygame.rect.Rect(*pos, 40, 40)
        self.texture = texture

    @property
    def cur_texture(self):
        cs = cos(self.time)
        surf = pygame.transform.scale(self.texture, (self.texture.get_width(), self.texture.get_height() + cs * 3))
        pygame.transform.rotate(surf, self.time)
        return surf

    def render(self, surf: pygame.Surface, camera_x, camera_y):
        x, y = mum_convert(self.rect.x, self.rect.y)
        self.time += 0.1
        self.time %= 3.15
        off_x = self.texture.get_width() // 2
        surf.blit(self.cur_texture, (x - camera_x - off_x, y - camera_y))
