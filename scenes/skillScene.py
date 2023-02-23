import csv
import os
from dataclasses import dataclass
from math import radians, cos, dist, sin
import numpy
import pygame

from player import Player
from skill import Skill
from utils.customFont import single_font
from utils.infoDisplay import generate_description


@dataclass(slots=True)
class SkillPoint:
    skill: Skill
    unlocks_skills: list[Skill]
    price: int
    cur_level: int
    max_level: int
    is_unlocked: bool

    def get_color(self):
        if not self.is_unlocked:
            return 200, 50, 50
        if self.cur_level == 0:
            return 150, 150, 150
        if self.cur_level == self.max_level:
            return 50, 200, 50
        return 0, 0, 200


@dataclass
class Point:
    x: float
    y: float
    z: float
    size: float
    sp: SkillPoint

    # another dataclass container ??? sounds lame. no colour tho

    @property
    def pos(self):
        return self.x, self.y, self.z

    @property
    def color(self):
        return self.sp.get_color()

    def project(self, W, H, scale):
        mx_size = min(W, H) // 2
        x, y, z = self.pos
        z += 1.5
        x /= z
        y /= z
        x *= scale
        y *= scale
        z /= scale
        x *= mx_size
        x += W // 2
        y *= mx_size
        y += H // 2
        return x, y, ((self.size / z) if z != 0 else 0)

    def rotate(self, anglex, angley, anglez):
        pos = numpy.array(self.pos)
        anglex = radians(anglex)
        angley = radians(angley)
        anglez = radians(anglez)
        cosa = cos(anglex)
        cosb = cos(angley)
        cosg = cos(anglez)
        sina = sin(anglex)
        sinb = sin(angley)
        sing = sin(anglez)
        rot_matrix = numpy.array([[cosb * cosg, sina * sinb * cosg - cosa * sing, sina * sing + cosa * sinb * cosg],
                                  [cosb * sing, cosa * cosg + sina * sinb * sing, cosa * sinb * sing - sina * cosg],
                                  [-sinb, sina * cosb, cosa * cosb]])
        pos = pos @ rot_matrix
        self.x, self.y, self.z = pos

    def normalize(self):
        a = self.x ** 2 + self.y ** 2 + self.z ** 2
        if a == 0:
            return
        k = a ** -0.5
        self.x *= k
        self.y *= k
        self.z *= k


class SkillScene:
    def __init__(self, screen: pygame.Surface, player: Player):
        pygame.init()
        self.screen = screen
        self.player = player
        self.W, self.H = screen.get_width() // 2, screen.get_height() // 2
        self.display = pygame.Surface((self.W, self.H))
        self.FPS = 120
        self.font = single_font('large_font')
        self.clock = pygame.time.Clock()
        self.points = [
            Point(1, 1, 1, 20, SkillPoint(Skill.BerBlock, [Skill.BerCrit], 1, 0, 5, True)),
            Point(1, 1.5, 1, 20, SkillPoint(Skill.BerCrit, [], 4, 0, 1, False)),
            Point(1, -1.5, 1, 20, SkillPoint(Skill.MiscMapDist, [Skill.MiscMapKeyPortal], 1, 0, 1, True)),
            Point(1, -1, 1, 20, SkillPoint(Skill.MiscMapKeyPortal, [], 1, 0, 1, False)),
            Point(0.9, -1.1, 1, 20, SkillPoint(Skill.MiscInventorySlot, [], 1, 0, 7, True)),
            Point(-1, 1, 1, 20, SkillPoint(Skill.TankHealth, [], 1, 0, 4, True))
        ]
        for p in self.points:
            p.normalize()
        self.scale = 1
        self.highlighted: None | Point = None

    def render_point(self, point):
        x, y, size = point.project(self.W, self.H, self.scale)
        if point is self.highlighted and type(point.color) != str:
            pygame.draw.circle(self.display, [min(255, i + 50) for i in point.color], (x, y), size)
        else:
            pygame.draw.circle(self.display, point.color, (x, y), size)

    def render(self):
        for point in self.points:
            self.render_point(point)
        point_count = generate_description('large_font', [], 'Points: ' + str(self.player.stats.skill_points))
        self.display.blit(point_count, (0, 0))
        if self.highlighted is None:
            return
        desc = self.cur_desc
        self.display.blit(desc, (self.W - desc.get_width(), 0))

    @property
    def cur_desc(self):
        sb = self.highlighted.sp
        name, desc = sb.skill.get_desc()
        d = {'Name': name,
             'Description': desc,
             'Level': f'{sb.cur_level} out of {sb.max_level}',
             'price': f'{sb.price}'}
        if sb.is_unlocked:
            return generate_description('large_font', d, 'Skill')
        ls = []
        for sk in self.points:
            sk = sk.sp
            if sb.skill in sk.unlocks_skills:
                ls.append(sk.skill.get_desc()[0])
        if ls:
            d['Requires'] = ', '.join(ls)
        return generate_description('large_font', d, 'Skill')

    def update(self):
        mx, my = pygame.mouse.get_pos()
        mx //= 2
        my //= 2
        for point in reversed(self.points):
            x, y, size = point.project(self.W, self.H, self.scale)
            if dist((x, y), (mx, my)) <= size:
                self.highlighted = point
                break
        else:
            self.highlighted = None
            return

    def rotate(self, dx, dy):
        ay = dx / 10
        ax = -dy / 10
        for point in self.points:
            point.rotate(ax, ay, 0)
        self.points.sort(key=lambda x: x.z, reverse=True)

    def on_click(self):
        if self.highlighted is None:
            return
        skill_box = self.highlighted.sp
        if skill_box.price > self.player.stats.skill_points:
            return
        if skill_box.cur_level == skill_box.max_level \
                or not skill_box.is_unlocked:
            return
        if skill_box.cur_level == 0:
            self.unlock_skills(skill_box)
        if skill_box.skill == Skill.MiscInventorySlot:
            self.player.inventory.add_slots(1)
        elif skill_box.skill == Skill.TankHealth:
            health, speed = skill_box.skill.get_stats()
            self.player.stats.max_health += health
            self.player.stats.speed -= speed
        self.player.stats.skill_points -= skill_box.price
        skill_box.cur_level += 1

    def unlock_skills(self, skill_box: SkillPoint):
        for skill in skill_box.unlocks_skills:
            for point in self.points:
                if point.sp.skill == skill:
                    point.sp.is_unlocked = True
                    break

    def get_skills(self, only_upgraded=False) -> list[tuple[Skill, int]]:
        ls = []
        for point in self.points:
            if only_upgraded and point.sp.cur_level == 0:
                continue
            ls.append((point.sp.skill, point.sp.cur_level))
        return ls

    def run(self):
        speed = (0, 0)
        click_coords = None
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                elif event.type == pygame.MOUSEWHEEL:
                    self.scale += event.y / 10
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                    click_coords = event.pos
                elif event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT and click_coords:
                    if dist(event.pos, click_coords) <= 2:
                        self.on_click()
            dx, dy = pygame.mouse.get_rel()
            if pygame.mouse.get_pressed()[0]:
                speed = (dx, dy)
            else:
                sx, sy = speed
                speed = sx * 0.97, sy * 0.97
            self.rotate(*speed)
            self.display.fill('black')
            self.update()
            self.render()
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            self.clock.tick(self.FPS)
            pygame.display.flip()

    def save(self):
        with open(os.path.join('save_files', 'skills.csv'), mode='w', newline='') as f:
            writer = csv.writer(f)
            for item in self.get_skills(True):
                skil, lvl = item
                writer.writerow((skil.value, lvl))

    def read(self):
        ls = []
        with open(os.path.join('save_files', 'skills.csv')) as f:
            reader = csv.reader(f)
            for skil, lvl in reader:
                ls.append((Skill(int(skil)), int(lvl)))
        for skil, lvl in ls:
            for point in self.points:
                if point.sp.skill == skil:
                    point.sp.cur_level = lvl
                    self.unlock_skills(point.sp)
                    break

