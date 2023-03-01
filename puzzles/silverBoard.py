import pygame

from puzzles.cellBoard import CellBoard


class SilverBoard(CellBoard):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.win_pos = (0, 0)
        self.player_pos = [width - 1, height - 1]

    def on_click(self, cell_coords):
        pass

    def move_right(self):
        x, y = self.player_pos
        row = self.board[y]
        for i in range(x, self.width):
            if row[i]:
                break
            x = i
        self.player_pos[0] = x

    def move_left(self):
        x, y = self.player_pos
        row = self.board[y]
        for i in range(x, -1, -1):
            if row[i]:
                break
            x = i
        self.player_pos[0] = x

    def move_down(self):
        x, y = self.player_pos
        for i in range(y, self.height):
            if self.board[i][x]:
                break
            y = i
        self.player_pos[1] = y

    def move_up(self):
        x, y = self.player_pos
        for i in range(y, -1, -1):
            if self.board[i][x]:
                break
            y = i
        self.player_pos[1] = y

    def check_win(self):
        if self.player_pos == self.win_pos:
            return True

    def render(self, surf: pygame.Surface):
        self._draw_outline(surf)
        for y, row in enumerate(self.board):
            for x, i in enumerate(row):
                if not i:
                    continue
                pygame.draw.rect(surf, 'white', (self.left + self.cell_size * x,
                                                 self.top + self.cell_size * y,
                                                 self.cell_size, self.cell_size))
        x, y = self.player_pos
        pygame.draw.circle(surf, 'red', (self.left + (x + 0.5) * self.cell_size,
                                         self.top + (y + 0.5) * self.cell_size), self.cell_size // 2)
        x, y = self.win_pos
        pygame.draw.circle(surf, 'blue', (self.left + (x + 0.5) * self.cell_size,
                                          self.top + (y + 0.5) * self.cell_size), self.cell_size // 2)

    @classmethod
    def from_board(cls, field: list[list[int]], player_pos, win_pos):
        h = len(field)
        w = len(field[0])
        board = cls(w, h)
        board.board = field
        board.win_pos = win_pos
        board.player_pos = player_pos
        return board
