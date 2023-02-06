from enum import Enum
from abc import ABC, abstractmethod

from interactables.baseInteractable import BaseInteractable
from loot.baseLoot import BaseLoot
from loot.keyItemLoot import KeyItemLoot
from utils.savingConst import SavingConstants


class PuzzleResult(Enum):
    Quit = 0
    Won = 1
    Lost = 2


class BasePuzzle(BaseInteractable, ABC):
    def __init__(self, pos, reward: list[BaseLoot] = None):
        self.reward = [] if reward is None else reward
        super().__init__(pos, [self.get_image()])
        self.hitbox_size = 50

    @abstractmethod
    def get_image(self):
        pass

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

    def serialize(self):
        ls = []
        for i in self.reward:
            for j in i.serialize():
                ls.append(j)
            ls.append('/n')
        return SavingConstants().get_const(type(self)), tuple(int(i) for i in self.pos), *ls

    @classmethod
    def read(cls, line):
        pos = eval(line[1])
        type_ = SavingConstants().get_type(int(line[0]))
        reward = []
        r = 2
        l = 2
        while r < len(line):
            if line[r] == '/n':
                item = SavingConstants().load(line[l:r])
                reward.append(item)
                l = r + 1
            r += 1
        return type_(pos, reward=reward)
