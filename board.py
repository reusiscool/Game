from pytmx.util_pygame import load_pygame
import os

from entity import Entity
from grassController import GrassController


class BoardReader:
    def __init__(self):
        self.reader = load_pygame(os.path.join('tiled', 'tsxFiles', 'test1.tmx'))

    def get_floor(self):
        pass

    def get_grass(self):
        pass


class Board:
    def __init__(self, tile_size):
        self.tile_size = tile_size
        self.map: dict[int, dict[int, list[Entity]]] = {}
        # self.reader = BoardReader()
        self.gc = GrassController()
        # for o in self.reader.get_layer_by_name('Floor').tiles():
        #     x, y, surf = o
        #     self.add(Obs((x * self.tile_size, y * self.tile_size), 1, surf))

    def add(self, obj: Entity):
        x, y = obj.pos
        x //= self.tile_size
        y //= self.tile_size
        if y not in self.map:
            self.map[y] = {}
        if x not in self.map[y]:
            self.map[y][x] = []
        self.map[y][x].append(obj)

    def pop(self, obj):
        x, y = obj.pos
        x //= self.tile_size
        y //= self.tile_size
        if y not in self.map:
            return
        if x not in self.map[y]:
            return
        self.map[y][x].remove(obj)

    def get_objects(self, pos, distance):
        x, y = pos
        x //= self.tile_size
        y //= self.tile_size
        distance //= self.tile_size
        ls = []
        for ny in range(y - distance, y + distance + 1):
            if ny not in self.map:
                continue
            for nx in range(x - distance, x + distance + 1):
                if nx not in self.map[ny]:
                    continue
                for b in self.map[ny][nx]:
                    ls.append(b)
        return ls

    def update(self, pos, distance):
        x, y = pos
        x //= self.tile_size
        y //= self.tile_size
        distance //= self.tile_size
        for ny in range(y - distance, y + distance + 1):
            if ny not in self.map:
                continue
            for nx in range(x - distance, x + distance + 1):
                if nx not in self.map[ny]:
                    continue
                for b in self.map[ny][nx]:
                    b.update(self)

    def render(self, surf, camera_x, camera_y, distance, pos_x, pos_y):
        x = int(pos_x // self.tile_size)
        y = int(pos_y // self.tile_size)
        print(x, y, '-', camera_x, camera_y)
        distance //= self.tile_size
        for ny in range(y - distance, y + distance + 1):
            if ny not in self.map:
                continue
            for nx in range(x - distance, x + distance + 1):
                if nx not in self.map[ny]:
                    continue
                ls = self.map[ny][nx]
                ls.sort(key=lambda o: o.x + o.y)
                for i in ls:
                    i.render(surf, camera_x, camera_y)

