import pygame
from abc import ABC, abstractmethod


class CellBoard(ABC):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_cell(self, mouse_pos):
        x = mouse_pos[0] - self.left
        if x < 0:
            print(x, mouse_pos)
            return None
        x //= self.cell_size
        if x >= self.width:
            print(x, mouse_pos, 1)
            return None
        y = mouse_pos[1] - self.top
        if y < 0:
            print(y, mouse_pos, 2)
            return None
        y //= self.cell_size
        if y >= self.height:
            print(y, mouse_pos, 3)
            return None
        return x, y

    @abstractmethod
    def on_click(self, cell_coords):
        pass

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if not cell:
            return
        self.on_click(cell)

    def _draw_outline(self, surf):
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(surf, 'white', (self.left + i * self.cell_size,
                                                 self.top + j * self.cell_size,
                                                 self.cell_size, self.cell_size), 1)

    @abstractmethod
    def render(self, surf):
        pass
