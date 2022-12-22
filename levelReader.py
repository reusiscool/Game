import pygame
import os

from level import Level


class LevelReader:
    def __init__(self, level):
        self.level = level
        self.level.generate()
        self.map_ = self.level.map_
        self.floor_img = pygame.image.load(os.path.join('tiled', 'Images', 'floor_tile.png'))
        self.floor_img.set_colorkey('black')
        self.floor_img = self.floor_img.convert()
        self.wall_img = pygame.image.load(os.path.join('tiled', 'Images', 'wall_tile.png'))
        self.wall_img.set_colorkey('white')
        self.wall_img = self.wall_img.convert()

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

    def get_enemies(self):
        return self.level.enimies

    def get_grass(self):
        pass
