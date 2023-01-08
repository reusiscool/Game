import pygame

from puzzles.cellBoard import CellBoard
from puzzles.ticLogic import TicTacToeLogic, Mark


class TicTacToeBoard(CellBoard):
    def __init__(self, position=None):
        super().__init__(3, 3)
        self.logic = TicTacToeLogic(position)
        self.board = self.logic.field
        self.cross_surf = self.get_cross()
        self.nought_surf = self.get_nought()

    def set_view(self, left, top, cell_size):
        super(TicTacToeBoard, self).set_view(left, top, cell_size)
        self.cross_surf = self.get_cross()
        self.nought_surf = self.get_nought()

    def get_cross(self) -> pygame.Surface:
        surf = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
        pygame.draw.line(surf, 'blue', (2, 2), (self.cell_size - 4, self.cell_size - 4), 2)
        pygame.draw.line(surf, 'blue', (2, self.cell_size - 4), (self.cell_size - 4, 2), 2)
        return surf

    def get_nought(self) -> pygame.Surface:
        surf = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
        pygame.draw.circle(surf, 'red', (0.5 * self.cell_size, 0.5 * self.cell_size),
                           self.cell_size // 2 - 2, 2)
        return surf

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
                    surf.blit(self.cross_surf, (self.left + i * self.cell_size,
                                                self.top + j * self.cell_size))
                elif self.board[j][i] == Mark.Nought:
                    surf.blit(self.nought_surf, (self.left + i * self.cell_size,
                                                 self.top + j * self.cell_size))
