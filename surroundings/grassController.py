from math import dist
from random import choice, randint
import pygame

from utils.converters import mum_convert
from .grass import Grass
from utils.utils import load_image


class GrassController:
    time_cap = 200

    def __init__(self, chunksize=10, tile_size=30, max_uniq=5):
        self.tile_size = tile_size
        self.max_uniq = max_uniq
        self.chunk_size = chunksize
        self.grass_text_list = [
            load_image('grass', f'grass_{i}.png', color_key='black') for i in range(6)
        ]
        self.cached_surfs = []
        self.grass_chunks: dict[tuple, list] = {}
        self.time = 0
        self.speed = 0.5
        self.addition = 15

    def put(self, pos, ind):
        dx = pos[0] // self.tile_size
        dy = pos[1] // self.tile_size
        pos1 = (dx, dy)
        if pos1 not in self.grass_chunks:
            self.grass_chunks[pos1] = []
        self.grass_chunks[pos1].append((pos, ind))

    def add_tile(self, pos):
        ind = len(self.cached_surfs)
        if ind >= self.max_uniq:
            self.put(pos, randint(0, self.max_uniq - 1))
            return
        self.cached_surfs.append([])
        self.cached_surfs[ind] = [None] * self.time_cap
        gr = []
        for i in range(0, self.chunk_size, 3):
            for j in range(0, self.chunk_size, 3):
                gr.append(Grass((i, j), choice(self.grass_text_list), self.time_cap // 4, 1))
        for i in range(self.time_cap):
            surf = pygame.Surface((self.chunk_size + self.addition * 2,
                                   self.chunk_size + self.addition * 2))
            surf.set_colorkey('black')
            for g in gr:
                g.update()
                g.render(surf, -self.addition, -self.addition)
            self.cached_surfs[ind][i] = surf
        self.put(pos, ind)

    def update(self):
        self.time = 0 if self.time >= self.time_cap - self.speed else self.time + self.speed

    def get_items(self, pos, distance, map_):
        x, y = pos
        ls = []
        for ny in range(int((y - distance) // self.tile_size),
                        int((y + distance) // self.tile_size) + 1):
            for nx in range(int((x - distance) // self.tile_size),
                            int((x + distance) // self.tile_size) + 1):
                pos = (nx, ny)
                if pos not in map_:
                    continue
                map_[pos].sort(key=lambda o: sum(o[0]))
                ls += map_[pos]
        return ls

    def retrieve_surfs(self, pos, distance, force_pos=None):
        res = []
        if force_pos is not None:
            for i in self.get_items(pos, distance, self.grass_chunks):
                s = self.cached_surfs[int(i[1])][int(self.time)]
                if dist(i[0], force_pos) <= 20:
                    newsurf = pygame.Surface((s.get_width(), s.get_height()))
                    newsurf.blit(s, (0, 0))
                    black_surf = pygame.Surface((s.get_width(), s.get_height()), pygame.SRCALPHA)
                    black_surf.fill((0, 0, 0, 100))
                    s = newsurf
                    s.blit(black_surf, (0, 0))
                    s.set_colorkey('black')
                res.append(GrassChunk(i[0], s, self.addition))
        else:
            for i in self.get_items(pos, distance, self.grass_chunks):
                res.append(GrassChunk(i[0],
                                      self.cached_surfs[int(i[1])][int(self.time)],
                                      self.addition))
        return sorted(res, key=lambda o: sum(o.pos))


class GrassChunk:
    def __init__(self, pos, img, addition):
        self.addition = addition
        self.texture = img
        self.pos = pos

    def tile_pos(self, tile_size):
        return self.pos[0] // tile_size, self.pos[1] // tile_size

    def render(self, surf: pygame.Surface, camera_x, camera_y):
        x, y = mum_convert(*self.pos)
        off_x = self.texture.get_width() // 2
        surf.blit(self.texture, (x - camera_x - off_x, y - camera_y - self.addition))
