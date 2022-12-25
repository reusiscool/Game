from random import choice, randint

import pygame
import os

from enemy import Enemy
from layout import Layout


class LevelReader:
    def __init__(self, level: Layout):
        self.level = level
        # self.level.generate()
        self.map_ = self.level.map_
        self.enemies = []
        self.player_room = (0, 0)
        self.floor_img = None
        self.wall_img = None
        self.load_pics()
        self.gen_mobs()
        self.level.write()

    def load_pics(self):
        self.floor_img = pygame.image.load(os.path.join('tiled', 'Images', 'floor_tile.png'))
        self.wall_img = pygame.image.load(os.path.join('tiled', 'Images', 'wall_tile.png'))
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

    def get_rand_room(self):
        return tuple(choice(self.level.rooms))

    def gen_mobs(self):
        self.player_room = self.get_rand_room()
        used = {self.player_room}
        for _ in range(len(self.level.rooms) // 2):
            p = self.get_rand_room()
            if p not in used:
                self.enemies += [p for _ in range(randint(3, 6))]
                used.add(p)

    def write(self):
        self.level.write()

    def get_enemies(self):
        return self.enemies

    def get_grass(self):
        pass
