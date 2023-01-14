from utils.savingConst import SavingConstants
from .baseItem import BaseItem
from utils.infoDisplay import generate_description
from utils.utils import load_image


class KeyItem(BaseItem):
    def __init__(self, lock_id):
        surf = load_image('key', 'key_item.png')
        desc = generate_description('large_font', {"Opens": lock_id}, 'Key')
        super().__init__(surf, desc)
        self.lock_id = lock_id

    def use(self, owner) -> bool:
        return False

    def serialize(self):
        return SavingConstants().get_const(KeyItem), self.lock_id
