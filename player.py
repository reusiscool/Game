from dataclasses import dataclass

from entity import Entity, EntityStats, Team
from move import Move
from utils import normalize, load_image
from sword import Sword, SwordStats
from ability import Ability


@dataclass(frozen=True, slots=True)
class PlayerStats:
    ents: EntityStats
    mana: int
    max_mana: int
    dash_cooldown: int
    dash_speed: int
    gold: int = 0


class Player(Entity):
    def __init__(self, hitbox_size, ps: PlayerStats):
        super().__init__(hitbox_size, ps.ents)
        self.dash_cooldown = ps.dash_cooldown
        self.dash_current_cooldown = 0
        self.dash_speed = ps.dash_speed
        self.mana = ps.mana
        self.max_mana = ps.max_mana
        self.gold = ps.gold
        sw_st1 = SwordStats(25, 45, 40, 40, 30)
        sw_st2 = SwordStats(10, 100, 45, 60, 60)
        imgs = [load_image('sword', 'sword.png', color_key='white')]
        self.weapon_list = [Sword(imgs, self, sw_st1),
                            Sword(imgs, self, sw_st2)]
        self.abbility = Ability([load_image('sword', 'sword.png', color_key='white')], self)
        self.try_attack = False
        self.try_sec_attack = False
        self.weapon_index = False
        self.looking_direction = (1, 1)
        self.team = Team.Player

    def render(self, surf, camera_x, camera_y):
        self.weapon_list[self.weapon_index].render(surf, camera_x, camera_y)
        super().render(surf, camera_x, camera_y)

    def change_weapon(self):
        self.weapon_index = not self.weapon_index

    def secondary_attack(self):
        self.try_sec_attack = True

    def attack(self):
        self.try_attack = True

    def calc_movement(self):
        dx = 0
        dy = 0
        for mov in self.move_q:
            if mov.own_speed:
                sx, sy = normalize(*mov.pos)
                dx += sx * self.speed * (1 - self.dash_current_cooldown / self.dash_cooldown) ** 0.5
                dy += sy * self.speed * (1 - self.dash_current_cooldown / self.dash_cooldown) ** 0.5
                continue
            dx += mov.dx
            dy += mov.dy
        for i in self.move_q:
            i.update()
        self.move_q = [i for i in self.move_q if i.duration > 0]
        return dx, dy

    def update(self, board):
        super().update(board)
        self.dash_current_cooldown = max(0, self.dash_current_cooldown - 1)
        self.weapon_list[self.weapon_index].update()
        self.abbility.update()
        if self.try_attack:
            self.weapon_list[self.weapon_index].attack(board)
            self.try_attack = False
        if self.try_sec_attack:
            self.abbility.attack(board)
            self.try_sec_attack = False

    def move_input(self, x, y):
        # self.looking_direction = (x, y)
        self.move_move(Move(x, y, own_speed=True, normalize=True))

    def dash(self, dx, dy):
        dx, dy = normalize(dx, dy)
        if self.dash_current_cooldown:
            return
        self.dash_current_cooldown = self.dash_cooldown
        self.move_q.append(Move(dx * self.dash_speed, dy * self.dash_speed, 10))
        self.move_q.append(Move(dx * self.dash_speed, dy * self.dash_speed, 7))
        self.move_q.append(Move(dx * self.dash_speed, dy * self.dash_speed, 4))
        self.move_q.append(Move(dx * self.dash_speed, dy * self.dash_speed, 2))
