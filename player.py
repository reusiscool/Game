from dataclasses import dataclass

from entity import Entity, EntityStats, Team
from move import Move
from utils import normalize, load_image
from sword import Sword, SwordStats
from ability import Ability


@dataclass(slots=True)
class PlayerStats(EntityStats):
    mana: int
    max_mana: int
    dash_cooldown: int
    dash_speed: int
    gold: int = 0

    def add_mana(self, amount):
        self.mana = min(self.max_mana, self.mana + amount)


class Player(Entity):
    def __init__(self, hitbox_size, ps: PlayerStats, inventory):
        super().__init__(hitbox_size, ps)
        self.inventory = inventory
        self.stats = ps
        self.dash_current_cooldown = 0
        sw_st1 = SwordStats(25, 45, 40, 40, 30)
        sw_st2 = SwordStats(10, 100, 45, 60, 60)
        imgs = [load_image('sword', 'sword.png', color_key='white')]
        self.weapon_list = [Sword(imgs, sw_st1),
                            Sword(imgs, sw_st2)]
        self.abbility = Ability([load_image('sword', 'sword.png', color_key='white')])
        self.try_attack = False
        self.try_sec_attack = False
        self.weapon_index = False
        self.looking_direction = (1, 1)
        self.is_interacting = False

    @property
    def team(self):
        return Team.Player

    def render(self, surf, camera_x, camera_y):
        self.weapon_list[self.weapon_index].render(surf, camera_x, camera_y, self)
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
                dx += sx * self.stats.speed * (1 - self.dash_current_cooldown / self.stats.dash_cooldown) ** 0.5
                dy += sy * self.stats.speed * (1 - self.dash_current_cooldown / self.stats.dash_cooldown) ** 0.5
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
            self.weapon_list[self.weapon_index].attack(board, self)
            self.try_attack = False
        if self.try_sec_attack:
            self.abbility.attack(board, self)
            self.try_sec_attack = False

    def move_input(self, x, y):
        self.move_move(Move(x, y, own_speed=True, normalize=True))

    def dash(self, dx, dy):
        dx, dy = normalize(dx, dy)
        if self.dash_current_cooldown:
            return
        self.dash_current_cooldown = self.stats.dash_cooldown
        self.move_q.append(Move(dx * self.stats.dash_speed, dy * self.stats.dash_speed, 10))
        self.move_q.append(Move(dx * self.stats.dash_speed, dy * self.stats.dash_speed, 7))
        self.move_q.append(Move(dx * self.stats.dash_speed, dy * self.stats.dash_speed, 4))
        self.move_q.append(Move(dx * self.stats.dash_speed, dy * self.stats.dash_speed, 2))

    def add_health(self, amount):
        self.stats.heal(amount)

    def add_mana(self, amount):
        self.stats.add_mana(amount)
