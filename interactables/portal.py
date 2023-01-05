import pygame

from interactables.baseInteractable import BaseInteractable
from items.keyItem import KeyItem
from utils.infoDisplay import generate_description


class Portal(BaseInteractable):
    def __init__(self, pos):
        surf = pygame.Surface((30, 30))
        surf.fill('green')
        self.locks = [0, 1]
        super().__init__(pos, [surf])
        self.hitbox_size = 50

    def get_desc(self):
        return generate_description('large_font', {f'Lock #{i}': 'locked' for i in self.locks}, 'Portal')

    def interact(self, obj, board):
        if not self.locks:
            obj.is_passing = True
            print('pass through')
            return
        for i, item in enumerate(reversed(obj.inventory.items)):
            if isinstance(item, KeyItem) and item.lock_id in self.locks:
                self.locks.remove(item.lock_id)
                obj.inventory.items.pop(len(obj.inventory.items) - i - 1)
                self.desc = self.get_desc()

    def render(self, surf, camera_x, camera_y):
        super().render(surf, camera_x, camera_y)
