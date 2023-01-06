import pygame

from utils.customFont import single_font


def generate_description(font_name, obj_stats: list | dict, title, color="black"):
    font = single_font(font_name)
    ls = [font.render(title)]
    if isinstance(obj_stats, dict):
        for val in obj_stats:
            ls.append(font.render(f'{val}: {obj_stats[val]}'))
    elif isinstance(obj_stats, list):
        for val in obj_stats:
            ls.append(font.render(val))
    sx = max(i.get_width() for i in ls)
    sy = (font.height + 1) * len(ls) - 1
    surf = pygame.Surface((sx, sy))
    surf.fill(color)
    for i, s in enumerate(ls):
        surf.blit(s, (0, i * (font.height + 1)))
    return surf
