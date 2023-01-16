from items.baseItem import BaseItem
from utils.infoDisplay import generate_description
from utils.savingConst import SavingConstants
from utils.utils import load_image


class ManaItem(BaseItem):
    def __init__(self, mana_amount=None):
        surf = load_image('mana', 'mana_item.png')
        self.mana_amount = mana_amount if mana_amount is not None else 10
        desc = generate_description('large_font', {'Mana amount': mana_amount}, 'Mana item')
        super().__init__(surf, desc)

    def use(self, owner):
        owner.add_mana(self.mana_amount)
        return True

    def serialize(self):
        return SavingConstants().get_const(ManaItem), self.mana_amount
