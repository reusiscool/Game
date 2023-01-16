from loot.baseItemLoot import BaseItemLoot
from items.healItem import HealItem
from utils.savingConst import SavingConstants
from utils.utils import load_image


class HealItemLoot(BaseItemLoot):
    def __init__(self, pos, amount=None):
        s = load_image('health', 'heal_item.png', color_key='white')
        super().__init__(pos, [s], HealItem(amount))

    @property
    def desc(self):
        return self.item.description

    def serialize(self):
        return SavingConstants().get_const(HealItemLoot), self.pos, self.item.heal_amount
