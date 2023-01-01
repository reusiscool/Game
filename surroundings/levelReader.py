from .layout import Layout
from .rooms import Room, RoomType
from utils.utils import load_image


class LevelReader:
    def __init__(self, level: Layout):
        self.level = level
        self.level.generate()
        self.map_ = self.level.map_
        self.enemies = []
        self.weapons = []
        self.player_room = (0, 0)
        self.floor_img = None
        self.wall_img = None
        self.load_pics()
        self.gen_mobs()
        self.level.write()

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
    def key_room(self):
        for i in self.level.rooms:
            if i.type_ == RoomType.Key:
                return i.rect.center

    def write(self):
        self.level.write()

    def get_enemies(self):
        return self.enemies

    def get_grass(self):
        pass
