from random import choice, randint
import pygame

from converters import mum_convert
from grass import Grass
from utils import load_image


class GrassController:
    time_cap = 100

    def __init__(self, tile_size=10, max_uniq=5):
        self.max_uniq = max_uniq
        self.chunk_size = tile_size
        self.grass_text_list = [load_image(f'grass_{i}.png', 'black') for i in range(6)]
        self.cached = dict()
        self.grass_chunks = []
        self.time = 0
        self.speed = 0.5
        self.addition = 15

    def add_tile(self, pos):
        ind = len(self.cached)
        if ind >= self.max_uniq:
            self.grass_chunks.append((pos, randint(0, self.max_uniq - 1)))
        self.cached[ind] = [None] * self.time_cap
        gr = []
        for i in range(0, self.chunk_size, 4):
            for j in range(0, self.chunk_size, 4):
                gr.append(Grass((i, j), choice(self.grass_text_list), self.time_cap // 4, 1))
        for i in range(self.time_cap):
            surf = pygame.Surface((self.chunk_size + self.addition * 2, self.chunk_size + self.addition * 2))
            surf.set_colorkey('black')
            for g in gr:
                g.update()
                g.render(surf, -self.addition, -self.addition)
            self.cached[ind][i] = surf
        self.grass_chunks.append((pos, ind))

    def update(self, force_pos=None):  # todo mb force_pos List
        self.time = 0 if self.time >= self.time_cap - self.speed else self.time + self.speed

    def retrieve_surfs(self):
        ls = []
        for i in self.grass_chunks:
            ls.append(GrassChunk(i[0], self.cached[i[1]][int(self.time)], self.addition))
        return ls


class GrassChunk:
    def __init__(self, pos, img, addition):
        self.addition = addition
        self.texture = img
        self.pos = pos

    def render(self, surf: pygame.Surface, camera_x, camera_y):
        x, y = mum_convert(*self.pos)
        off_x = self.texture.get_width() // 2
        surf.blit(self.texture, (x - camera_x - off_x, y - camera_y - self.addition))
