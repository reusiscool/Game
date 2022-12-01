import random
import pygame

from converters import mum_convert


class Grass:
    def __init__(self, pos, texture: pygame.Surface, max_angle=25):
        self.max_angle = max_angle
        self.pos = pos
        self.time_y = random.randint(0, 6)
        self.time_x = random.randint(0, 50) - 5
        self.v_x = 0.5
        self.rect = pygame.rect.Rect(*pos, 40, 40)
        self.texture = texture
        self.max_dist2 = 20 ** 2

    @property
    def cur_texture(self):
        surf = pygame.transform.rotate(self.texture, self.time_x)
        pygame.transform.rotate(surf, self.time_y)
        return surf

    def shadow(self, surf):
        shade = pygame.Surface(surf.get_size())
        shade_amt = 100 * abs(self.time_x) // 90
        shade.set_alpha(shade_amt)
        surf.blit(shade, (0, 0))

    def apply_force(self, player_pos):
        d = (player_pos[0] - self.pos[0]) ** 2 + (player_pos[1] - self.pos[1]) ** 2
        if d > self.max_dist2:
            return
        alpha = (1 - d / self.max_dist2) * 70
        self.time_x = alpha if sum(self.pos) > sum(player_pos) else -alpha

    def update(self):
        if self.time_x > self.max_angle:
            self.v_x = -abs(self.v_x)
        elif self.time_x < -self.max_angle:
            self.v_x = abs(self.v_x)
        self.time_x += self.v_x

    def render(self, surf: pygame.Surface, camera_x, camera_y):
        x, y = map(int, mum_convert(self.rect.x, self.rect.y))
        new_s = self.cur_texture
        self.shadow(new_s)
        surf.blit(new_s, (x - new_s.get_width() // 2 - camera_x,
                          y - new_s.get_height() // 2 - camera_y))
