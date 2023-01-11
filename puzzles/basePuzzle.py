from enum import Enum
from abc import ABC, abstractmethod
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
