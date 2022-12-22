from math import dist
import pygame
import numpy
from random import randint
from scipy.spatial import Delaunay
from scipy.sparse.csgraph import minimum_spanning_tree

from utils import draw_rect_line


class Level:
    def __init__(self, name, tile_size, size):
        self.size = size
        self.name = name
        self.tile_size = tile_size
        self.map_ = [[]]
        self.enimies = []

    def generate(self):
        avg_room_size = 4

        room_num = self.size // avg_room_size * 2

        ls = []
        for _ in range(room_num):
            while True:
                w, h = randint(avg_room_size - 1, avg_room_size + 1), randint(avg_room_size - 1, avg_room_size + 1)
                r = pygame.Rect(randint(0, self.size - 1 - w), randint(0, self.size - 1 - h), w, h)
                for i in ls:
                    if i.colliderect(r):
                        break
                else:
                    break
            ls.append(r)
        map_ = numpy.zeros((self.size, self.size))
        for r in ls:
            x1, y1 = r.topleft
            x2, y2 = r.bottomright
            map_[y1:y2, x1:x2] = 1

        points = numpy.array([i.center for i in ls])
        tri = Delaunay(points)
        mtrx = numpy.zeros((tri.npoints, tri.npoints))

        for con in tri.simplices:
            a, b, c = con
            mtrx[a, b] = mtrx[b, a] = dist(points[a], points[b])
            mtrx[c, b] = mtrx[b, c] = dist(points[c], points[b])
            mtrx[a, c] = mtrx[c, a] = dist(points[a], points[c])

        min_tree = minimum_spanning_tree(mtrx).toarray().astype(int)
        for y, row in enumerate(min_tree):
            for x, val in enumerate(row):
                if val:
                    for x5, y5 in draw_rect_line(points[x], points[y]):
                        map_[y5, x5] = 1
        for x5, y5 in draw_rect_line((0, 0), points[0]):
            map_[y5, x5] = 1
        for i in map_:
            print(*i)
        self.map_ = map_

        for i in points:
            self.enimies += [i] * randint(3, 7)

    @classmethod
    def read_from(cls, name, path, tile_size):
        pass

    def write(self):
        pass
