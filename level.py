from math import dist
import pygame
import numpy
from random import randint
from scipy.spatial import Delaunay
from scipy.sparse.csgraph import minimum_spanning_tree


class Level:
    def __init__(self, name, tile_size, size):
        self.size = size
        self.name = name
        self.tile_size = tile_size

    def generate(self):
        ls = []
        for _ in range(3):
            while True:
                r = pygame.Rect(randint(0, self.size - 1), randint(0, self.size - 1), randint(3, 5), randint(3, 5))
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

        min_tree = minimum_spanning_tree(mtrx)
        for i in min_tree.toarray():
            # p1, p2 = points[i.tocoo().row], points[i.tocoo().col]
            print(i)

        return map_

    @classmethod
    def read_from(cls, name, path, tile_size):
        pass

    def write(self):
        pass
