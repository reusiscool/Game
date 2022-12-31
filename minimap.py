import pygame
from rooms import Room, RoomType


class Minimap:
    def __init__(self, map_, rooms: list[Room], textures: dict[int, pygame.Surface] = None):
        self.rooms = rooms
        self.map_ = map_
        self.size = len(map_)
        self.ts = 10
        if textures is None:
            self.textures = self.get_pics()
        else:
            self.textures = textures
        self.player_pos = (0, 0)
        self.gap = self.ts * 15
        self.surf = pygame.Surface((self.size * self.ts + self.gap * 2, self.size * self.ts + self.gap * 2))
        self.surf.fill('black')

    def get_pics(self):
        d = {}
        colors = ['green', 'white', 'yellow', 'grey', (0, 0, 1), 'purple', 'blue', 'purple', 'white', 'red']
        for i in range(10):
            s = pygame.Surface((self.ts, self.ts))
            s.fill(colors[i])
            d[i] = s
        return d

    def update(self, board):
        x, y = board.player.tile_pos(board.tile_size)
        dist = board.update_distance // board.tile_size
        for y1 in range(max(y - dist, 0), min(y + dist, self.size)):
            for x1 in range(max(x - dist, 0), min(x + dist, self.size)):
                if not self.map_[y1][x1]:
                    self.surf.blit(self.textures[self.map_[y1][x1]],
                                   (x1 * self.ts + self.gap, y1 * self.ts + self.gap))
                    continue
                for r in self.rooms:
                    if r.rect.collidepoint(x1, y1):
                        self.surf.blit(self.textures[r.type_.value],
                                       (x1 * self.ts + self.gap, y1 * self.ts + self.gap))
                        break
                else:
                    self.surf.blit(self.textures[self.map_[y1][x1]], (x1 * self.ts + self.gap, y1 * self.ts + self.gap))

        px, py = board.player.pos
        px = px / board.tile_size * self.ts
        py = py / board.tile_size * self.ts

        self.player_pos = (px, py)

    def get_surf(self):
        px, py = self.player_pos
        dist = self.ts * 15
        surf = self.surf.subsurface(px - dist + self.gap, py - dist + self.gap, 2 * dist, 2 * dist)
        surf.set_at((0, 0), 'black')
        surf = pygame.transform.rotate(surf, -45)
        surf.set_colorkey('black')
        return surf

    def render(self, surf: pygame.Surface):
        s = self.get_surf()
        surf.blit(s, ((surf.get_width() - s.get_width()) // 2, (surf.get_height() - s.get_height()) // 2))
