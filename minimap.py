import csv
import os
import pygame

from surroundings.rooms import RoomType
from utils.infoDisplay import generate_description


class Minimap:
    def __init__(self, board, read=False):
        self.rooms = board.reader.level.room_list
        self.map_ = board.reader.map_
        self.colors = ['green', 'white', 'yellow', 'grey', 'black', 'purple',
                  'blue', 'purple', 'white', 'red']
        self.size = len(self.map_)
        self.ts = 10
        self.textures = self.get_pics()
        self.player_pos = (0, 0)
        self.gap = self.ts * 15
        self.surf = pygame.Surface((self.size * self.ts + self.gap * 2,
                                    self.size * self.ts + self.gap * 2), pygame.SRCALPHA)
        self.revealed_rooms: list[RoomType] = board.player.stats.revealed_rooms
        self.revealed_map = self._read() if read else [[False] * len(self.map_) for _ in range(len(self.map_))]
        self.reveal_dist: int = None
        self.max_reveal_distance = 7

    def _draw_empty(self, x, y):
        self.surf.blit(self.textures[1],
                       (x * self.ts + self.gap, y * self.ts + self.gap))

    def _draw_wall(self, x, y):
        self.surf.blit(self.textures[0],
                       (x * self.ts + self.gap, y * self.ts + self.gap))

    def _draw_room(self, x, y, room_type):
        self.surf.blit(self.textures[room_type.value],
                       (x * self.ts + self.gap, y * self.ts + self.gap))

    def _read(self):
        with open(os.path.join('save_files', 'minimap.csv')) as f:
            reader = csv.reader(f)
            ls = []
            for row in reader:
                if not row:
                    continue
                ls.append([int(i) for i in row])
        for y1 in range(len(self.map_)):
            for x1 in range(len(self.map_)):
                if not ls[y1][x1]:
                    continue
                if not self.map_[y1][x1]:
                    self._draw_wall(x1, y1)
                    continue
                for r in self.rooms:
                    if not r.rect.collidepoint(x1, y1):
                        continue
                    if r.type_ not in self.revealed_rooms:
                        self._draw_empty(x1, y1)
                        break
                    self._draw_room(x1, y1, r.type_)
                    break
                else:
                    self._draw_empty(x1, y1)
        return ls

    def get_pics(self):
        d = {}
        for i in range(10):
            s = pygame.Surface((self.ts, self.ts))
            s.fill(self.colors[i])
            d[i] = s
        return d

    def update(self, board):
        x, y = board.player.tile_pos(board.tile_size)
        d = self.reveal_dist = min(self.max_reveal_distance, board.player.stats.reveal_distance)
        self.revealed_rooms = board.player.stats.revealed_rooms

        for y1 in range(max(y - d, 0), min(y + d, self.size)):
            for x1 in range(max(x - d, 0), min(x + d, self.size)):
                self.revealed_map[y1][x1] = True
                if not self.map_[y1][x1]:
                    self._draw_wall(x1, y1)
                    continue
                for r in self.rooms:
                    if not r.rect.collidepoint(x1, y1):
                        continue
                    if r.type_ not in self.revealed_rooms:
                        self._draw_empty(x1, y1)
                        break
                    self._draw_room(x1, y1, r.type_)
                    break
                else:
                    self._draw_empty(x1, y1)

        px, py = board.player.pos
        px = px / board.tile_size * self.ts
        py = py / board.tile_size * self.ts

        self.player_pos = (px, py)

    def get_surf(self):
        px, py = self.player_pos
        dist = self.ts * 15
        surf = self.surf.subsurface(px - dist + self.gap, py - dist + self.gap, 2 * dist, 2 * dist)
        surf = pygame.transform.rotate(surf, -45)
        return surf

    def get_desc(self):
        d = {'Reveal distance': self.reveal_dist,
             'Reveal distance caps at': self.max_reveal_distance}
        if self.revealed_rooms:
            for r in self.revealed_rooms:
                d[r] = self.colors[r.value]
        return generate_description('large_font', d, 'Map stats')

    def render(self, surf: pygame.Surface):
        s = self.get_surf()
        surf.blit(s, ((surf.get_width() - s.get_width()) // 2,
                      (surf.get_height() - s.get_height()) // 2))
        desc = self.get_desc()
        pygame.draw.circle(surf, 'yellow', (surf.get_width() // 2, surf.get_height() // 2), 3)
        surf.blit(desc, (surf.get_width() - desc.get_width(), 0))

    def save(self):
        ls = []
        for row in self.revealed_map:
            ls.append([int(i) for i in row])
        with open(os.path.join('save_files', 'minimap.csv'), 'w') as f:
            writer = csv.writer(f)
            writer.writerows(ls)
