import os
from math import dist
from random import randint

from utils.savingConst import SavingConstants
from .entityGen import EntityGen
from .layout import Layout
from .obs import Wall, Obs
from .rooms import RoomType
from utils.utils import load_image


class LevelReader:
    def __init__(self, tile_size, next_lvl=False):
        self.tile_size = tile_size
        self.level: Layout
        self.entity_reader: EntityGen
        self._init(next_lvl)
        self.grass = []
        self.gen_grass()
        self.map_ = self.level.map_
        self.floor_img = load_image('tiles', 'floor_tile.png', color_key='black')
        self.wall_img = load_image('tiles', 'wall_tile.png', color_key='white')

    def _init(self, generate_new):
        with open(os.path.join('levels', 'GameState.txt')) as f:
            k = int(f.readline())
        if k == 0 or generate_new:
            lvl_num = k + 1
            self.level = Layout(lvl_num, SavingConstants().level_size[lvl_num - 1])
            while True:
                self.level.generate()
                if RoomType.Player in (i.type_ for i in self.level.room_list):
                    break
            self.entity_reader = EntityGen(lvl_num, self.tile_size)
            self.entity_reader.generate(self.level.room_list)
            with open(os.path.join('levels', 'GameState.txt'), 'w') as f:
                f.write(str(lvl_num))
        else:
            self.level = Layout.read_from(k)
            self.entity_reader = EntityGen.read(k, self.tile_size)

    def load(self, board):
        for item in self.entity_reader.noncolliders:
            board.add_noncollider(item)
        for en in self.entity_reader.enemies:
            board.add_enemy(en)
        for x, y in self.get_walls():
            board.add_item(Wall((x * self.tile_size, y * self.tile_size), 0, self.wall_img),
                           board.collider_map)
            board.add(Obs((x * self.tile_size, y * self.tile_size), self.tile_size))
        for x, y in self.get_floor():
            obj = Obs((x * self.tile_size, y * self.tile_size), 0, self.floor_img)
            board.add_item(obj, board.floor_map)

    def get_floor(self):
        for y, row in enumerate(self.map_):
            for x, cell in enumerate(row):
                if cell == 1:
                    yield x, y

    def get_walls(self):
        for y, row in enumerate(self.map_):
            for x, cell in enumerate(row):
                if cell == 0:
                    yield x, y

    @property
    def player_room(self):
        for room in self.level.room_list:
            if room.type_ == RoomType.Player:
                return room.rect.center

    def write(self, entity_list):
        self.level.write()
        self.entity_reader.write(entity_list)

    def grass_circle(self, cx, cy, r, room):
        for y in range(cy - r - 100, cy + r + 100, 150):
            for x in range(cx - r - 100, cx + r + 100, 150):
                if dist((cx, cy), (x, y)) > r:
                    continue
                c1, c2 = x / 1000, y / 1000
                if room.rect.collidepoint(c1, c2):
                    self.grass.append((c1, c2))

    def gen_grass(self):
        for room in self.level.room_list:
            if room.type_ not in (RoomType.Combat, RoomType.Puzzle, RoomType.Null, RoomType.Player):
                continue
            W = room.rect.width * 1000
            H = room.rect.height * 1000
            left = room.rect.left * 1000
            right = room.rect.right * 1000
            top = room.rect.top * 1000
            bottom = room.rect.bottom * 1000
            for _ in range(3):
                cx, cy = room.rect.center
                cx *= 1000
                cy *= 1000
                cx += randint(0, W) - W // 2
                cy += randint(0, H) - H // 2
                for _ in range(20):
                    r = 200
                    cx += randint(0, r * 4) - r * 2
                    cy += randint(0, r * 4) - r * 2
                    if cx < left:
                        cx += r * 3 // 2
                    elif cx > right:
                        cx -= r * 3 // 2
                    if cy < top:
                        cy += r * 3 // 2
                    elif cy > bottom:
                        cy -= r * 3 // 2
                    self.grass_circle(cx, cy, r, room)
