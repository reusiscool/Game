from interactables.baseInteractable import BaseInteractable
from items.keyItem import KeyItem
from utils.infoDisplay import generate_description
from utils.savingConst import SavingConstants
from utils.utils import load_image


class Portal(BaseInteractable):
    def __init__(self, pos, locks=None):
        surf = load_image('portal', 'portal.png', color_key='white')
        surf2 = load_image('portal', 'locked_portal.png', color_key='white')
        self.locks = [0, 1] if locks is None else locks
        super().__init__(pos, [surf, surf2])
        self.hitbox_size = 50

    def get_desc(self):
        return generate_description('large_font',
                                    {f'Lock #{i}': 'locked' for i in self.locks},
                                    'Portal')

    def render(self, surf, camera_x, camera_y):
        self.image_index = not self.locks
        super().render(surf, camera_x, camera_y)

    def interact(self, obj, board):
        if not self.locks:
            obj.is_passing = True
            return
        for i in range(len(obj.inventory.items) - 1, -1, -1):
            item = obj.inventory.items[i]
            if isinstance(item, KeyItem) and item.lock_id in self.locks:
                self.locks.remove(item.lock_id)
                obj.inventory.items.pop(i)
                self.desc = self.get_desc()

    def serialize(self):
        return SavingConstants().get_const(type(self)), tuple(self.locks),\
               (int(self.x), int(self.y))

    @classmethod
    def read(cls, line):
        locks = list(eval(line[1]))
        pos = eval(line[2])
        return cls(pos, locks)
