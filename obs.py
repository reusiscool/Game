import pygame
from converters import mum_convert


class Obs:
    def __init__(self, pos, width=0, img=None):
        self.x, self.y = pos
        self.pos = pos
        self.rect = pygame.rect.Rect(*pos, width, width)
        if not img:
            self.texture = pygame.Surface((40, 40))
            self.paint()
        else:
            self.texture = img

    def update(self, *args):
        pass

    def paint(self):
        pygame.draw.circle(self.texture, 'yellow', (20, 20), 20)

    def render(self, surf: pygame.Surface, camera_x, camera_y):
        x, y = mum_convert(self.rect.x, self.rect.y)
        off_x = self.texture.get_width() // 2
        surf.blit(self.texture, (x - camera_x - off_x, y - camera_y))
