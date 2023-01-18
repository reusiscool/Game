from random import randint

from mixer import Mixer
from utils.savingConst import SavingConstants
from weapons.baseAbility import AbilityStats, BaseAbility
from weapons.baseProjectile import BaseProjectile
from utils.utils import normalize, load_image


class Ability(BaseAbility):
    def __init__(self, ast: AbilityStats):
        img_l = [load_image('ability', f'ability{i}.png', color_key='white') for i in range(6)]
        super().__init__(ast, img_l + list(reversed(img_l)))

    def attack(self, board, owner):
        if self.current_cooldown or owner.stats.mana < self.stats.cost:
            return
        Mixer().on_ability()
        owner.stats.mana -= self.stats.cost
        self.current_cooldown = self.stats.cooldown
        vx, vy = normalize(*owner.looking_direction)
        vx *= 8
        vy *= 8
        b = BaseProjectile(owner.pos, 10, self.image_list, 420,
                           owner, (vx, vy), self.stats.damage)
        board.add_projectile(b)

    def serialize(self):
        return SavingConstants().get_const(Ability), self.stats.cooldown,\
               self.stats.cost, self.stats.damage

    @classmethod
    def generate(cls, rarity, lvl):
        raw_stats = []
        min_stats = []
        for min_stat, raw_stat in SavingConstants().get_stats(Ability, lvl):
            min_stats.append(min_stat)
            raw_stats.append(raw_stat)
        score = SavingConstants().avg_weapon_score[rarity] * 3
        stat_score = [0] * 5
        ind = 0
        while score > 0:
            if stat_score[ind] >= 100:
                ind = (ind + 1) % 3
                continue
            roll = randint(0, 3)
            stat_score[ind] += roll
            score -= roll
            ind = (ind + 1) % 3
        stats = [raw_stats[i] * stat_score[i] // 100 + min_stats[i] for i in range(3)]
        stats[0] = max(100 - stats[0], 0)
        stats[1] = max(0, 100 - stats[1])
        return cls(AbilityStats(*stats))
