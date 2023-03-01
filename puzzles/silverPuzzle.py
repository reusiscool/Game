from random import choice
import pygame
import csv
import os

from puzzles.basePuzzle import PuzzleResult, BasePuzzle
from puzzles.silverBoard import SilverBoard
from utils.infoDisplay import generate_description
from utils.singleton import Singleton
from utils.utils import load_image


class SilverReader(metaclass=Singleton):
    def __init__(self):
        self.sets: list[tuple] = []
        self._read()

    def _read(self):
        with open(os.path.join('puzzles', 'silverSets.txt')) as f:
            reader = csv.reader(f)
            res = []
            while True:
                k = next(reader)
                if k[0] == '/n':
                    break
                px, py, ex, ey, w, h = map(int, k)
                temp = []
                for i in range(h):
                    temp.append([int(i) for i in next(reader)])
                res.append(([px, py], [ex, ey], temp))
            self.sets = res


class SilverPuzzle(BasePuzzle):
    def __init__(self, pos, reward):
        super().__init__(pos, reward)
        player_pos, exit_pos, field = choice(SilverReader().sets)
        self.board = SilverBoard.from_board(field, player_pos, exit_pos)

    def get_image(self):
        return load_image('puzzles', 'liar.png', color_key='white')

    def get_desc(self):
        return generate_description('large_font', [], 'Silverfish puzzle')

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.board.move_right()
        elif keys[pygame.K_LEFT]:
            self.board.move_left()
        elif keys[pygame.K_DOWN]:
            self.board.move_down()
        elif keys[pygame.K_UP]:
            self.board.move_up()

    def run(self) -> PuzzleResult:
        screen = pygame.display.get_surface()
        clock = pygame.time.Clock()
        self.board.resize_to_fit(screen)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return PuzzleResult.Quit
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return PuzzleResult.Quit
            if self.board.check_win():
                return PuzzleResult.Won
            self.handle_input()
            screen.fill('black')
            self.board.render(screen)
            pygame.display.flip()
            clock.tick(60)
