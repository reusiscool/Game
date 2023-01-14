from abc import ABC, abstractmethod
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


class BaseShop(BaseInteractable, ABC):
    def __init__(self, pos, rarity: int, image_list: list[pygame.Surface], level=0, goods=None):
        """rarity is an integer from 0 to 3 inclusive"""
        self.rarity = rarity
        super().__init__(pos, image_list)
        self.goods = self._gen_goods(level) if goods is None else goods
        self.buttons: list[Button] = []
        self.hitbox_size = 50

    @abstractmethod
    def _list_of_goods(self, rarity, level):
        return ...

    def _gen_goods(self, level):
        goods = []
        for _ in range(3):
            item, stats = choice(self._list_of_goods(self.rarity, level))
            *stats, price = stats
            x, y = self.pos
            item = item((x + 60, y + 60), *stats)
            goods.append((item, price))
        return goods

    def _gen_buttons(self, w, h):
        self.buttons.clear()
        for i, good in enumerate(self.goods):
            if good is None:
                continue
            item, price = good
            r = pygame.Rect(w // 2 - w // 10 + (i - 1) * 3 * w // 10,
                            h // 2 - w // 10, w // 5, w // 5)
            self.buttons.append(Button(i, r, item.desc, price))

    @abstractmethod
    def get_desc(self):
        return ...

    def buy(self, board, ind: int):
        item, price = self.goods[ind]
        if price > board.player.stats.gold:
            return
        board.player.stats.gold -= price
        board.add_noncollider(item)
        self.goods[ind] = None
        self.buttons[ind] = None

    def interact(self, obj, board):
        screen = pygame.display.get_surface()
        clock = pygame.time.Clock()
        w, h = screen.get_size()
        if not self.buttons and any(self.goods):
            self._gen_buttons(w, h)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for btn in self.buttons:
                        if btn is None:
                            continue
                        if btn.rect.collidepoint(*event.pos):
                            self.buy(board, btn.id_)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
            screen.fill('black')
            for btn in self.buttons:
                if btn is not None:
                    btn.render(screen)
            pygame.display.flip()
            clock.tick(60)

    def serialize(self):
        ls = []
        for i in range(3):
            if self.goods[i] is None:
                ls.append([])
                continue
            item1, price1 = self.goods[i]
            item1 = item1.serialize()
            ls.append([*item1, price1])
        return SavingConstants().get_const(type(self)), self.pos, self.rarity, \
            *ls[0], '/n', *ls[1], '/n', *ls[2]
