import pygame

from puzzles.cellBoard import CellBoard
from puzzles.ticLogic import TicTacToeLogic, Mark


class TicTacToeBoard(CellBoard):
    def __init__(self, position=None):
        super().__init__(3, 3)
        self.logic = TicTacToeLogic(position)
        self.board = self.logic.field

    def on_click(self, cell_coords):
        self.logic.move(*cell_coords)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if not cell:
            return self.logic.state
        self.on_click(cell)
        return self.logic.state

    def render(self, surf):
        self._draw_outline(surf)
        for i in range(3):
            for j in range(3):
                if self.board[j][i] == Mark.Cross:
                    pygame.draw.line(surf, 'blue', (self.left + i * self.cell_size + 2,
                                                    self.top + j * self.cell_size + 2),
                                     (self.left + i * self.cell_size + self.cell_size - 4,
                                      self.top + j * self.cell_size + self.cell_size - 4), 2)
                    pygame.draw.line(surf, 'blue', (self.left + i * self.cell_size + 2,
                                                    self.top + j * self.cell_size + self.cell_size - 4),
                                     (self.left + i * self.cell_size + self.cell_size - 4,
                                      self.top + j * self.cell_size + 2), 2)
                elif self.board[j][i] == Mark.Nought:
                    pygame.draw.circle(surf, 'red', (self.left + (i + 0.5) * self.cell_size,
                                                     self.top + (j + 0.5) * self.cell_size), self.cell_size // 2 - 2, 2)


