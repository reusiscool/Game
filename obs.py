import pygame
from converters import mum_convert


class Obs:
    def __init__(self, pos=(100, 100)):
        self.pos = pos
        self.rect = pygame.rect.Rect(*pos, 40, 40)
        self.texture = pygame.Surface((40, 40))
        self.paint()

    def paint(self):
        pygame.draw.circle(self.texture, 'yellow', (20, 20), 20)

    def render(self, surf: pygame.Surface, camera_x, camera_y):
        x, y = mum_convert(self.rect.x, self.rect.y)
        off_x = self.texture.get_width() // 2
        surf.blit(self.texture, (x - camera_x - off_x, y - camera_y))
