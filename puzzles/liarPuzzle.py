import csv
import os
from dataclasses import dataclass
from random import choice
import pygame

from loot.baseLoot import BaseLoot
from puzzles.basePuzzle import BasePuzzle, PuzzleResult
from utils.infoDisplay import generate_description
from utils.singleton import Singleton
from utils.utils import load_image

names = ['Bob', 'Top', 'Rob']


class LiarReader(metaclass=Singleton):
    def __init__(self):
        self.sets = []
        self._read()

    def _read(self):
        with open(os.path.join('puzzles', 'liarSets.csv')) as f:
            ls = []
            for i in csv.reader(f):
                ls.append(i)
        self.sets = ls


@dataclass(slots=True)
class Button:
    id_: int
    rect: pygame.Rect
    desc: str | pygame.Surface

    def __post_init__(self):
        self.desc = self.desc.replace('[Person 1]', names[0])
        self.desc = self.desc.replace('[Person 2]', names[1])
        self.desc = self.desc.replace('[Person 3]', names[2])
        self.desc = generate_description('large_font', self.desc.split('/n'), names[self.id_])

    def render(self, surf: pygame.Surface):
        pygame.draw.rect(surf, 'white', self.rect)
        if self.rect.collidepoint(*pygame.mouse.get_pos()):
            desc_rect = self.rect.move((self.rect.width - self.desc.get_width()) // 2, -100)
            surf.blit(self.desc, desc_rect)


class LiarPuzzle(BasePuzzle):
    def __init__(self, pos, reward: list[BaseLoot] = None, *_):
        super().__init__(pos, reward)
        self.buttons: list[Button] = []
        self.correct = None

    def read_sets(self, w, h):
        ls = choice(LiarReader().sets)
        dx = w // 7
        for i, info in enumerate(ls[:3]):
            rct = pygame.Rect(w // 2 - dx * (2.5 - i * 2), h * 3 // 5, dx, dx)
            self.buttons.append(Button(i, rct, info))
        self.correct = int(ls[3])

    def get_image(self):
        return load_image('puzzles', 'liar.png', color_key='white')

    def run(self) -> PuzzleResult:
        screen = pygame.display.get_surface()
        clock = pygame.time.Clock()
        w, h = screen.get_size()
        if self.correct is None:
            self.read_sets(w, h)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return PuzzleResult.Quit
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for btn in self.buttons:
                        if btn.rect.collidepoint(*event.pos):
                            if btn.id_ == self.correct:
                                return PuzzleResult.Won
                            else:
                                return PuzzleResult.Lost
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return PuzzleResult.Quit
            screen.fill('black')
            for i in self.buttons:
                i.render(screen)
            pygame.display.flip()
            clock.tick(60)

    def get_desc(self):
        return generate_description('large_font', [], 'Liar-Knight puzzle')
