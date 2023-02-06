from dataclasses import dataclass

from weapons.sword import Sword, SwordStats


@dataclass(frozen=True)
class GoldenSwordStats(SwordStats):
    gold_drop: int


class GoldenSword(Sword):
    def __init__(self, sword_stats: GoldenSwordStats):
        super().__init__(sword_stats)

    def kill_drop(self, board, owner):
        owner += self.stats.gold_drop

    @staticmethod
    def get_stats_type():
        return GoldenSwordStats

    def serialize(self):
        return *super().serialize(), self.stats.gold_drop


@dataclass(frozen=True)
class ManaSwordStats(SwordStats):
    mana_drop: int


class ManaSword(Sword):
    def __init__(self, sword_stats: ManaSwordStats):
        super().__init__(sword_stats)

    def hit_drop(self, board, owner):
        if owner.stats.mana <= owner.stats.max_mana // 2:
            owner.stats.add_mana(self.stats.mana_drop)

    @staticmethod
    def get_stats_type():
        return ManaSwordStats

    def serialize(self):
        return *super().serialize(), self.stats.mana_drop

