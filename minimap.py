import pygame
import numpy


class Minimap:
    def __init__(self, map_):
        self.map_ = map_
        self.revealed_map = numpy.zeros((len(map_), len(map_[0])))

    def update(self, board):
        pos = board.player.tile_pos(board.tile_size)

