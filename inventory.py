import pygame

from items.baseItem import BaseItem


class Inventory:
    def __init__(self, size: int, surf_size):
        self.size = size
        self.items: list[BaseItem] = []
        self.rects: list[pygame.Rect] = self.gen_rects(surf_size)
        self.cur_desc = None

    def resize(self, surf_size):
        self.rects: list[pygame.Rect] = self.gen_rects(surf_size)

    @property
    def is_full(self):
        return len(self.items) >= self.size

    def gen_rects(self, surf_size):
        sx, sy = surf_size
        item_size = sx // (self.size * 1.4)
        x_off = sx // self.size
        ans = []
        for i in range(self.size):
            y = sy // 2 - item_size // 2
            x = sx // 2 + x_off * (i - 3) - item_size // 2
            ans.append(pygame.Rect(x, y, item_size, item_size))
        return ans

    def get_item(self, mpos):
        mx, my = mpos
        mx *= 0.5
        my *= 0.5
        for i, r in enumerate(self.rects):
            if r.collidepoint(mx, my):
                index = i
                break
        else:
            return None
        if index >= len(self.items):
            index = None
        return index

    def add_item(self, item: BaseItem) -> bool:
        """:return: whether the item fits to the inventory"""
        if len(self.items) >= self.size:
            return False
        self.items.append(item)
        return True

    def discard_item(self, mpos):
        index = self.get_item(mpos)
        if index is None:
            return
        self.items.pop(index)

    def use_item(self, mpos, owner):
        index = self.get_item(mpos)
        if index is None:
            return
        if self.items[index].use(owner):
            self.items.pop(index)

    def update(self, mpos):
        index = self.get_item(mpos)
        if index is None:
            self.cur_desc = None
            return
        self.cur_desc = self.items[index].description

    def render(self, surf: pygame.Surface):
        shadow_focus = pygame.Surface(surf.get_size(), flags=pygame.SRCALPHA)
        shadow_focus.fill((0, 0, 0, 100))
        surf.blit(shadow_focus, (0, 0))
        for r in self.rects:
            pygame.draw.rect(surf, 'grey', r)
        for i, item in enumerate(self.items):
            s = pygame.transform.scale(item.icon, self.rects[i].size)
            surf.blit(s, self.rects[i])
        if self.cur_desc is not None:
            surf.blit(self.cur_desc, (surf.get_width() - self.cur_desc.get_width(), 0))
