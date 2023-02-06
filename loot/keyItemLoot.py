from loot.baseItemLoot import BaseItemLoot
from items.keyItem import KeyItem
from utils.savingConst import SavingConstants
from utils.utils import load_image


class KeyItemLoot(BaseItemLoot):
    def __init__(self, pos, id_):
        s = load_image('key', 'key_item.png', color_key='white')
        super().__init__(pos, [s], KeyItem(id_))

    def serialize(self):
        return SavingConstants().get_const(type(self)),\
               (int(self.x), int(self.y)), self.item.lock_id

    @classmethod
    def read(cls, line):
        pos = eval(line[1])
        id_ = eval(line[2])
        return cls(pos, id_)
