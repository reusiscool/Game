from math import dist
from random import randint, choice

from .layout import Layout
from .rooms import Room, RoomType
from utils.utils import load_image


class LevelReader:
    def __init__(self, level: Layout):
        self.level = level
        while True:
            self.level.generate()
            if RoomType.Player in (i.type_ for i in self.level.rooms):
                break
        self.traps = []
        self.grass = []
        self.gen_grass()
        self.gen_traps()
        self.map_ = self.level.map_
        self.enemies = []
        self.weapons = []
        self.player_room = (0, 0)
        self.floor_img = None
        self.wall_img = None
        self.load_pics()
        self.gen_mobs()
        self.level.write()

    def get_rooms(self, room_type: RoomType) -> list[Room]:
        for i in self.level.rooms:
            if i.type_ == room_type:
                yield i

    def load_pics(self):
        self.floor_img = load_image('tiles', 'floor_tile.png')
        self.wall_img = load_image('tiles', 'wall_tile.png')
        self.wall_img.set_colorkey('white')
        self.wall_img = self.wall_img.convert()
        self.floor_img.set_colorkey('black')
        self.floor_img = self.floor_img.convert()

    def get_floor(self):
        for y, row in enumerate(self.map_):
            for x, cell in enumerate(row):
                if cell == 1:
                    yield x, y, self.floor_img

    def get_walls(self):
        for y, row in enumerate(self.map_):
            for x, cell in enumerate(row):
                if cell == 0:
                    yield x, y, self.wall_img

    def gen_mobs(self):
        for i in self.level.rooms:
            i: Room
            if i.type_ == RoomType.Player:
                self.player_room = i.rect.center
            elif i.type_ == RoomType.Combat:
                self.enemies.append(i.rect.center)
                self.enemies.append(i.rect.center)
                self.enemies.append(i.rect.center)
            elif i.type_ == RoomType.Weapon:
                self.weapons.append(i.rect.center)

    @property
    def key_rooms(self):
        c = 0
        for i in self.level.rooms:
            if i.type_ == RoomType.Key:
                yield i.rect.center, c
                c += 1

    @property
    def portal_room(self):
        for i in self.level.rooms:
            if i.type_ == RoomType.Portal:
                return i.rect.center

    def write(self):
        self.level.write()

    def get_enemies(self):
        return self.enemies

    def grass_circle(self, cx, cy, r, room):
        for y in range(cy - r - 100, cy + r + 100, 150):
            for x in range(cx - r - 100, cx + r + 100, 150):
                if dist((cx, cy), (x, y)) > r:
                    continue
                c1, c2 = x / 1000, y / 1000
                if room.rect.collidepoint(c1, c2):
                    self.grass.append((c1, c2))

    def gen_traps(self):
        for room in self.level.rooms:
            if room.type_ not in (RoomType.Combat, RoomType.Null, RoomType.Puzzle):
                continue
            for x in range(room.rect.x, room.rect.right):
                for y in range(room.rect.y, room.rect.bottom):
                    if randint(0, 10):
                        continue
                    self.traps.append((x, y))

    def gen_grass(self):
        for room in self.level.rooms:
            if room.type_ not in (RoomType.Combat, RoomType.Puzzle, RoomType.Null, RoomType.Player):
                continue
            W = room.rect.width * 1000
            H = room.rect.height * 1000
            for _ in range(5):
                cx, cy = room.rect.center
                cx *= 1000
                cy *= 1000
                cx += randint(0, W) - W // 2
                cy += randint(0, H) - H // 2
                for _ in range(3):
                    r = randint(300, 700)
                    cx += randint(0, r * 2) - r
                    cy += randint(0, r * 2) - r
                    if cx < room.rect.left * 1000:
                        cx += r * 3 // 2
                    elif cx > room.rect.right * 1000:
                        cx -= r * 3 // 2
                    if cy < room.rect.top * 1000:
                        cy += r * 3 // 2
                    elif cy > room.rect.bottom * 1000:
                        cy -= r * 3 // 2
                    self.grass_circle(cx, cy, r, room)
