import pygame
import csv
import os
import numpy

from loot.baseLoot import BaseLoot
from puzzles.ticBoard import TicTacToeBoard
from puzzles.ticLogic import Mark
from puzzles.basePuzzle import BasePuzzle, PuzzleResult
from puzzles.ticLogic import GameState
from utils.infoDisplay import generate_description


class TicTacToePuzzle(BasePuzzle):
    def __init__(self, pos, id_, reward: list[BaseLoot] = None, level=0):
        super().__init__(pos, id_, reward)
        fk, self.draw_wins = self.read_sets(level)
        self.board = TicTacToeBoard(fk)

    def read_sets(self, level):
        with open(os.path.join('puzzles', 'ticSets.csv')) as f:
            reader = csv.reader(f)
            ls = []
            for line in reader:
                ls.append(line)
            while True:
                ind = numpy.random.normal(max(level, 8), 2.7)
                if ind < 0 or ind >= 9:
                    continue
                break
            ls = ls[int(ind)]
        pos = [int(i) for i in ls[:9]]
        pos = [[Mark(pos[i + j * 3]) for i in range(3)] for j in range(3)]
        return pos, int(ls[9])

    def run(self) -> PuzzleResult:
        screen = pygame.display.get_surface()
        clock = pygame.time.Clock()
        res = self.board.logic.state
        w, h = screen.get_size()
        cs = h // 5
        self.board.set_view(int(w // 2 - cs * 1.5), cs, cs)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if res != GameState.on_going:
                        if res == GameState.won or res == GameState.drawn and self.draw_wins:
                            return PuzzleResult.Won
                        return PuzzleResult.Lost
                    res = self.board.get_click(event.pos)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return PuzzleResult.Quit
            screen.fill('black')
            self.board.render(screen)
            pygame.display.flip()
            clock.tick(60)

    def get_desc(self):
        return generate_description('large_font', {}, 'Tic-Tac-Toe puzzle')
