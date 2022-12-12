import pygame
from random import randint
from converters import mum_convert


class Particle:
    def __init__(self, pos: tuple):
        self.radius = randint(3, 6)
        self.x = pos[0] + randint(0, 2) - 3
        self.y = pos[1] + randint(0, 2) - 3
        self.sp_x = (randint(0, 400) - 200) / 100
        self.sp_y = (randint(0, 400) - 200) / 100
        self.g = 0.1

    def get_surf(self):
        r = self.radius * 2
        surf = pygame.Surface((r * 2, r * 2))
        pygame.draw.circle(surf, (30, 30, 50), (r, r), r)
        surf.set_colorkey('black')
        return surf

    def render(self, screen: pygame.Surface, camera_x, camera_y):
        if self.radius <= 0:
            return False
        x, y = mum_convert(self.x, self.y)
        s = self.get_surf()
        pygame.draw.circle(screen, 'white', (x - camera_x, y - camera_y), self.radius)
        screen.blit(s, (x - camera_x - self.radius * 2, y - camera_y - self.radius * 2),
                    special_flags=pygame.BLEND_RGB_ADD)
        self.sp_y += self.g
        self.sp_x += self.g
        self.radius -= self.g
        self.x += self.sp_x
        self.y += self.sp_y
        return True
