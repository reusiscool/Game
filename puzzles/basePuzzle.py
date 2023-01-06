from enum import Enum
from abc import ABC, abstractmethod
import pygame

from interactables.baseInteractable import BaseInteractable
from loot.baseLoot import BaseLoot


class PuzzleResult(Enum):
    Quit = 0
    Won = 1
    Lost = 2


class BasePuzzle(BaseInteractable, ABC):
    def __init__(self, pos, reward: list[BaseLoot]):
        self.reward = reward
        surf = pygame.Surface((50, 50))
        surf.fill('pink')
        super().__init__(pos, [surf])
        self.hitbox_size = 50

    @abstractmethod
    def run(self) -> PuzzleResult:
        return ...

    def interact(self, obj, board):
        res = self.run()
        if res != PuzzleResult.Quit:
            board.pop_loot(self)
        if res == PuzzleResult.Won:
            for lt in self.reward:
                board.add_noncollider(lt)
