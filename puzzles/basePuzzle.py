from enum import Enum
from abc import ABC, abstractmethod
from random import randint, choice

import pygame

from interactables.baseInteractable import BaseInteractable
from loot.baseLoot import BaseLoot
from loot.keyItemLoot import KeyItemLoot
from utils.savingConst import SavingConstants


class PuzzleResult(Enum):
    Quit = 0
    Won = 1
    Lost = 2


class BasePuzzle(BaseInteractable, ABC):
    def __init__(self, pos, id_, reward: list[BaseLoot] = None):
        self.reward = [] if reward is None else reward
        surf = pygame.Surface((50, 50))
        surf.fill('pink')
        super().__init__(pos, [surf])
        self.id = id_
        self.hitbox_size = 50

    @abstractmethod
    def run(self) -> PuzzleResult:
        return ...

    def interact(self, obj, board):
        res = self.run()
        if res != PuzzleResult.Quit:
            board.pop_loot(self)
        if res == PuzzleResult.Won:
            if self.id:
                board.add_noncollider(KeyItemLoot(self.pos, self.id))
            for lt in self.reward:
                board.add_noncollider(lt)

    def serialize(self):
        return SavingConstants().get_const(BasePuzzle), tuple(int(i) for i in self.pos), self.id

    @classmethod
    def read(cls, line, level):
        from puzzles.ticPuzzle import TicTacToePuzzle
        from puzzles.liarPuzzle import LiarPuzzle
        from loot.moneyLoot import MoneyLoot
        if len(line) == 3:
            id_ = int(line[2])
        else:
            id_ = None
        pos = eval(line[1])
        puzzle = choice((TicTacToePuzzle, LiarPuzzle))
        reward = []
        for _ in range(3):
            if randint(0, 1):
                reward.append(MoneyLoot(pos, SavingConstants().gold_drop[level]))
        return puzzle(pos, id_, reward=reward)
