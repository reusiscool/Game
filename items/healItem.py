
from items.baseItem import BaseItem
from utils.infoDisplay import generate_description
from utils.savingConst import SavingConstants
from utils.utils import load_image


class HealItem(BaseItem):
    def __init__(self, heal_amount=None):
        surf = load_image('health', 'heal_item.png')
        self.heal_amount = heal_amount if heal_amount is not None else 10
        desc = generate_description('large_font', {'Heals': self.heal_amount}, 'Heal item')
        super().__init__(surf, desc)

    def use(self, owner):
        owner.add_health(self.heal_amount)
        return True

    def serialize(self):
        return SavingConstants().get_const(HealItem), self.heal_amount
