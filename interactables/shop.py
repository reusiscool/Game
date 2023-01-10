from random import choice

import pygame

from interactables.baseInteractable import BaseInteractable
from utils.infoDisplay import generate_description
from utils.savingConst import SavingConstants


class Button:
    def __init__(self, id_: int, rect: pygame.Rect, item_desc, price):
        self.rect = rect
        self.id_ = id_
        self.desc = item_desc
        self.price = price
        self.desc2 = generate_description('large_font', [], f'Price: {price}')

    def render(self, surf: pygame.Surface):
        pygame.draw.rect(surf, 'white', self.rect)
        if self.rect.collidepoint(*pygame.mouse.get_pos()):
            desc_rect = self.rect.move((self.rect.width - self.desc.get_width()) // 2, -100)
            surf.blit(self.desc, desc_rect)
            desc2_rect = self.rect.move((self.rect.width - self.desc2.get_width()) // 2, -150)
            surf.blit(self.desc2, desc2_rect)


class Shop(BaseInteractable):
    def __init__(self, pos, rarity: int, level, goods=None):
        """rarity is an integer from 0 to 3 inclusive"""
        self.rarity = rarity
        surf = pygame.Surface((50, 50))
        surf.fill('brown')
        image_list = [surf]
        super().__init__(pos, image_list)
        self.goods = self._gen_goods(level) if goods is None else goods
        self.buttons: list[Button] = []

    def _gen_goods(self, level):
        s = SavingConstants()
        ls = s.get_shop_items(self.rarity, level)
        goods = []
        for _ in range(3):
            item, stats = choice(ls)
            *stats, price = stats
            item = item(self.pos, *stats)
            goods.append((item, price))
        return goods

    def _gen_buttons(self, w, h):
        self.buttons.clear()
        for i, good in enumerate(self.goods):
            item, price = good
            r = pygame.Rect(w // 2 - w // 10 + (i - 1) * 3 * w // 10, h // 2 - w // 10, w // 5, w // 5)
            self.buttons.append(Button(i, r, item.desc, price))

    def get_desc(self):
        return generate_description('large_font', [], 'Shop')

    def buy(self, board, ind):
        item, price = self.goods[ind]
        if price > board.player.stats.gold:
            return
        board.player.stats.gold -= price
        board.add_noncollider(item)

    def interact(self, obj, board):
        screen = pygame.display.get_surface()
        clock = pygame.time.Clock()
        w, h = screen.get_size()
        if not self.buttons:
            self._gen_buttons(w, h)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for btn in self.buttons:
                        if btn.rect.collidepoint(*event.pos):
                            self.buy(board, btn.id_)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
            screen.fill('black')
            for btn in self.buttons:
                btn.render(screen)
            pygame.display.flip()
            clock.tick(60)
