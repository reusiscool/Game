import os
import pygame


generated_fonts = {}


def single_font(font_name: str):
    if font_name in generated_fonts:
        return generated_fonts[font_name]
    instance = CustomFont(font_name)
    generated_fonts[font_name] = instance
    return instance


class CustomFont:
    def __init__(self, font_name: str):
        self.font_name = font_name
        self.height = 0
        self.characters: dict[str, pygame.Surface] = {}
        order = self.read_order()
        self.read_font(order)
        self.space_width = 3
        self.spacing = 1

    def read_order(self):
        with open(os.path.join('.', 'imgs', 'fonts', self.font_name + '.txt')) as f:
            ls = f.readline().strip('\n')
        return ls

    def read_font(self, order):
        surf = pygame.image.load(os.path.join('.', 'imgs', 'fonts',
                                              self.font_name + '.png')).convert()
        self.height = surf.get_height()
        cur_width = 0
        cur_char = 0
        for x in range(surf.get_width()):
            if surf.get_at((x, 0))[0] == 127:
                s = surf.subsurface(x - cur_width, 0, cur_width, self.height)
                s.set_colorkey('black')
                self.characters[order[cur_char]] = s
                cur_width = 0
                cur_char += 1
            else:
                cur_width += 1

    def render(self, text, color='black', alpha=False):
        sx = 0
        sy = self.height
        for i in text:
            if i == ' ':
                sx += self.space_width + 1
            elif i not in self.characters:
                continue
            else:
                sx += self.characters[i].get_width() + 1
        sx -= 1
        if alpha:
            surf = pygame.Surface((sx, sy), pygame.SRCALPHA)
        else:
            surf = pygame.Surface((sx, sy))
            surf.fill(color)
        x = 0
        for char in text:
            if char == ' ':
                x += self.space_width + self.spacing
                continue
            if char not in self.characters:
                continue
            surf.blit(self.characters[char], (x, 0))
            x += self.characters[char].get_width() + self.spacing
        return surf
