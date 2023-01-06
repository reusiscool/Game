from enum import Enum
from copy import deepcopy
from random import choice


class Mark(Enum):
    Null = 0
    Nought = -1
    Cross = 1

    def flip(self):
        if self == Mark.Null:
            return Mark.Null
        return Mark.Cross if self == Mark.Nought else Mark.Nought


class GameState(Enum):
    lost = 0
    drawn = 1
    won = 2
    on_going = 3


def has_won(field, move_symb):
    row = any(all(j == move_symb for j in field[i]) for i in range(3))
    col = any(all(field[j][i] == move_symb for j in range(3)) for i in range(3))
    dia1 = all(field[i][i] == move_symb for i in range(3))
    dia2 = all(field[i][2-i] == move_symb for i in range(3))
    if any((row, col, dia1, dia2)):
        return True
    return False


def has_drawn(field):
    return all(all(i != Mark.Null for i in field[j]) for j in range(3))


def minimax(field: list[list], move_mark: Mark):
    res = set()
    for i in range(3):
        for j in range(3):
            if field[j][i] == Mark.Null:
                field1 = deepcopy(field)
                field1[j][i] = move_mark
                if has_won(field1, move_mark):
                    return move_mark
                if has_drawn(field1):
                    res.add(Mark.Null)
                    continue
                res.add(minimax(field1, move_mark.flip()))
    if move_mark in res:
        return move_mark
    if Mark.Null in res:
        return Mark.Null
    return move_mark.flip()


class TicTacToeLogic:
    def __init__(self, field=None):
        self.field = [[Mark.Null] * 3 for _ in range(3)] if field is None else field
        self.verify_field()
        self.cur_mark = self.eval_move_order()
        self.player_mark = self.cur_mark
        self.state = GameState.on_going

    def verify_field(self):
        if len(self.field) != 3:
            raise ValueError(self.field)
        for i in self.field:
            if len(i) != 3:
                raise ValueError(self.field)

    def eval_move_order(self):
        cr = 0
        nd = 0
        for i in range(3):
            for j in range(3):
                if self.field[j][i] == Mark.Nought:
                    nd += 1
                elif self.field[j][i] == Mark.Cross:
                    cr += 1
        if cr == nd:
            return Mark.Cross
        if cr - nd == 1:
            return Mark.Nought
        print(self.field)
        raise ValueError

    def ai_move(self):
        variants = []
        for i in range(3):
            for j in range(3):
                if self.field[i][j] == Mark.Null:
                    field1 = deepcopy(self.field)
                    field1[i][j] = self.cur_mark
                    if has_won(field1, self.cur_mark):
                        variants.append([self.cur_mark, (i, j)])
                        continue
                    fav = minimax(field1, self.cur_mark.flip())
                    variants.append([fav, (i, j)])
        ch_vars = []
        for fav, move in variants:
            if fav == self.cur_mark:
                i, j = move
                ch_vars.append((i, j))
        if ch_vars:
            i, j = choice(ch_vars)
            self.field[i][j] = self.cur_mark
            return
        for fav, move in variants:
            if fav == Mark.Null:
                i, j = move
                ch_vars.append((i, j))
        if ch_vars:
            i, j = choice(ch_vars)
            self.field[i][j] = self.cur_mark
            return
        _, move = choice(variants)
        i, j = move
        self.field[i][j] = self.cur_mark

    def game_checks(self):
        if has_won(self.field, self.cur_mark):
            if self.cur_mark == self.player_mark:
                self.state = GameState.won
            else:
                self.state = GameState.lost
        elif has_drawn(self.field):
            self.state = GameState.drawn

    def move(self, x, y):
        if self.state != GameState.on_going:
            return self.state
        if self.field[y][x] != Mark.Null:
            return self.state
        self.field[y][x] = self.cur_mark
        self.game_checks()
        self.cur_mark = self.cur_mark.flip()
        if self.state != GameState.on_going:
            return self.state
        self.ai_move()
        self.game_checks()
        self.cur_mark = self.cur_mark.flip()
        return self.state
