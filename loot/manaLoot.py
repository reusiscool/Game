from loot.baseLoot import BaseLoot
from player import Player
from utils.infoDisplay import generate_description
from utils.savingConst import SavingConstants
from utils.utils import load_image


class ManaLoot(BaseLoot):
    def __init__(self, pos, amount=None):
        surf = load_image('mana', 'mana_loot.png', color_key='white')
        super().__init__(pos, [surf])
        self.amount = amount if amount is not None else 10

    @property
    def desc(self):
        return generate_description('large_font', {'Mana amount': self.amount}, "Mana loot")

    def add_amount(self, obj: Player, board):
        obj.add_mana(self.amount)

    def serialize(self):
        return SavingConstants().get_const(ManaLoot), self.pos, self.amount
