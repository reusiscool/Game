import pygame
from math import ceil

from items.baseItem import BaseItem


class Inventory:
    def __init__(self, size: int, surf_size):
        self.size = size
        self.items: list[BaseItem] = []
        self.w, self.h = surf_size
        self.rects: list[pygame.Rect] = self.gen_rects()
        self.cur_desc = None

    def resize(self, surf_size):
        self.w, self.h = surf_size
        self.rects: list[pygame.Rect] = self.gen_rects()

    def add_slots(self, amount):
        if amount <= 0:
            raise ValueError(amount)
        self.size += amount
        self.size = min(25, self.size)
        self.rects = self.gen_rects()

    @property
    def is_full(self):
        return len(self.items) >= self.size

    def gen_rects(self):
        items_ina_row = 5
        item_size = min(self.w, self.h) // (items_ina_row * 1.5)
        row_num = ceil(self.size / items_ina_row)
        gap_x = (self.w - item_size * items_ina_row) // (items_ina_row * 4)
        gap_y = (self.h - item_size * items_ina_row) // (items_ina_row * 3)
        ans = []
        for i in range(row_num):
            y = self.h // 2 - item_size // 2 + (item_size + gap_y) * (i - (row_num - 1) / 2)
            iinr = min(self.size - items_ina_row * i, items_ina_row)
            for j in range(iinr):
                x = self.w // 2 - item_size // 2 + (item_size + gap_x) * (j - (iinr - 1) / 2)
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
