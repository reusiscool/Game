from copy import deepcopy
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
from utils.utils import load_image
from utils.singleton import Singleton


class SetsReader(metaclass=Singleton):
    def __init__(self):
        self.tic_sets = []
        self.read_sets()

    def read_sets(self):
        self.tic_sets.clear()
        with open(os.path.join('puzzles', 'ticSets.csv')) as f:
            reader = csv.reader(f)
            for line in reader:
                pos = [int(i) for i in line[:9]]
                pos = [[Mark(pos[i + j * 3]) for i in range(3)] for j in range(3)]
                self.tic_sets.append((pos, int(line[9])))

    def get_random(self, level):
        while True:
            ind = numpy.random.normal(max(level, 8), 2.7)
            if ind < 0 or ind >= 9:
                continue
            break
        return self.tic_sets[int(ind)]


class TicTacToePuzzle(BasePuzzle):
    def __init__(self, pos, reward: list[BaseLoot], level=0):
        super().__init__(pos, reward)
        fk, self.draw_wins = SetsReader().get_random(level)
        self.board = TicTacToeBoard(deepcopy(fk))

    def get_image(self):
        return load_image('puzzles', 'tic_tac_toe.png', color_key='white')

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
                    return PuzzleResult.Quit
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
