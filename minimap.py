import pygame
import numpy


class Minimap:
    def __init__(self, map_, textures: dict[int, pygame.Surface] = None):
        self.map_ = map_
        self.size = len(map_)
        self.revealed_map = numpy.zeros((len(map_), len(map_)), dtype=numpy.int8)
        self.ts = 10
        if textures is None:
            self.textures = self.get_pics()
        else:
            self.textures = textures
        self.player_pos = (0, 0)

    def get_pics(self):
        t0 = pygame.Surface((self.ts, self.ts))
        t0.fill('green')
        t1 = pygame.Surface((self.ts, self.ts))
        t1.fill('white')
        return {0: t0, 1: t1}

    def update(self, board):
        x, y = board.player.tile_pos(board.tile_size)
        dist = board.update_distance // board.tile_size - 1

        for y1 in range(max(y - dist, 0), min(y + dist, self.size)):
            for x1 in range(max(x - dist, 0), min(x + dist, self.size)):
                self.revealed_map[y1, x1] = 1

        px, py = board.player.pos
        px = px / board.tile_size * self.ts
        py = py / board.tile_size * self.ts

        self.player_pos = (px, py)

    def get_surf(self):
        px, py = self.player_pos
        dist = self.ts * 15
        gap = self.ts * 15
        surf = pygame.Surface((self.size * self.ts + gap * 2, self.size * self.ts + gap * 2))
        surf.fill('black')
        for y, row in enumerate(self.revealed_map):
            for x, val in enumerate(row):
                if val:
                    surf.blit(self.textures[self.map_[y][x]], (x * self.ts + gap, y * self.ts + gap))
        surf = surf.subsurface(px - dist + gap, py - dist + gap, 2 * dist, 2 * dist)
        surf.set_at((0, 0), 'black')
        surf = pygame.transform.rotate(surf, -45)
        surf.set_colorkey('black')
        return surf

    def render(self, surf: pygame.Surface):
        s = self.get_surf()
        surf.blit(s, ((surf.get_width() - s.get_width()) // 2, (surf.get_height() - s.get_height()) // 2))
