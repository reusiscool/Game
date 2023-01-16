from items.manaItem import ManaItem
from loot.baseItemLoot import BaseItemLoot
from utils.savingConst import SavingConstants
from utils.utils import load_image


class ManaItemLoot(BaseItemLoot):
    def __init__(self, pos, amount=None):
        s = load_image('mana', 'mana_item.png', color_key='white')
        super().__init__(pos, [s], ManaItem(amount))

    @property
    def desc(self):
        return self.item.description

    def serialize(self):
        return SavingConstants().get_const(ManaItemLoot), self.pos, self.item.mana_amount
