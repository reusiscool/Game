import pygame
from utils.converters import mum_convert


class Obs:
    def __init__(self, pos, width=0, img=None):
        self.x, self.y = pos
        self.rect = pygame.rect.Rect(*pos, width, width)
        self.texture = img

    @property
    def off_x(self):
        return self.texture.get_width() // 2

    @property
    def off_y(self):
        return 0

    @property
    def pos(self):
        return self.x, self.y

    def tile_pos(self, tile_size):
        return self.x // tile_size, self.y // tile_size

    def render(self, surf: pygame.Surface, camera_x, camera_y):
        if not self.texture:
            return
        x, y = mum_convert(self.rect.x, self.rect.y)
        surf.blit(self.texture, (x - camera_x - self.off_x, y - camera_y - self.off_y))


class Wall(Obs):
    def __init__(self, pos, width, img=None):
        super().__init__(pos, width, img)

    @property
    def off_y(self):
        return 60
