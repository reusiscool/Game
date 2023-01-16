from loot.baseLoot import BaseLoot
from utils.savingConst import SavingConstants
from utils.utils import load_image


class MoneyLoot(BaseLoot):
    def __init__(self, pos, amount):
        surf = load_image('gold', 'gold.png', color_key='white')
        super().__init__(pos, [surf])
        self.amount = amount

    def add_amount(self, obj, board):
        obj.stats.gold += self.amount

    def serialize(self):
        return SavingConstants().get_const(MoneyLoot), self.pos, self.amount
