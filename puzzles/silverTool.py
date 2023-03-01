import os
from dataclasses import dataclass, field
import pygame
import csv

from puzzles.silverBoard import SilverBoard
from utils.customFont import single_font


class SilverToolBoard(SilverBoard):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.cur_placement = 0

    def on_click(self, cell_coords):
        x, y = cell_coords
        if self.cur_placement == 0:
            self.board[y][x] = not self.board[y][x]
        elif self.cur_placement == 2:
            self.win_pos = list(cell_coords)
        else:
            self.player_pos = list(cell_coords)


@dataclass
class Button:
    id: int
    rect: pygame.Rect
    txt: pygame.Surface
    active: bool = field(init=False)

    def __post_init__(self):
        self.resize_txt()
        self.active = False

    def resize_txt(self):
        sx, sy = self.rect.size
        x, y = self.txt.get_size()
        k = min(sx / x, sy / y) * 0.85
        x *= k
        y *= k
        self.txt = pygame.transform.scale(self.txt, (x, y))

    def render(self, screen):
        if self.active:
            pygame.draw.rect(screen, 'white', self.rect)
        else:
            pygame.draw.rect(screen, 'grey', self.rect)
        x = self.rect.centerx - self.txt.get_width() // 2
        y = self.rect.centery - self.txt.get_height() // 2
        screen.blit(self.txt, (x, y))

    def collide_point(self, point) -> bool:
        return self.rect.collidepoint(*point)


class SilverTool:
    def __init__(self, screen: pygame.Surface, board_width=None, board_height=None):
        self.screen = screen
        self.font = single_font('large_font')
        if board_width is None:
            self.board = self._read()
        else:
            self.board = SilverToolBoard(board_width, board_height)
        self.W, self.H = self.screen.get_size()
        bh = self.H // 5
        bw = bh * 2
        btn1 = Button(0, pygame.Rect(self.W - bw, bh // 2, bw, bh), self.font.render('Blocks', alpha=True))
        btn2 = Button(1, pygame.Rect(self.W - bw, (self.H - bh) // 2, bw, bh), self.font.render('Player', alpha=True))
        btn3 = Button(2, pygame.Rect(self.W - bw, self.H - bh * 3 // 2, bw, bh), self.font.render('Exit', alpha=True))
        btn1.active = True
        self.btns = [btn1, btn2, btn3]
        self.exit = Button(-1, pygame.Rect(0, self.H - bh, bw, bh), self.font.render('No Saving', alpha=True))

    def _read(self):
        with open(os.path.join('puzzles', 'tempSilver.csv')) as f:
            reader = csv.reader(f)
            px, py, ex, ey, *_ = map(int, next(reader))
            ls = []
            for row in reader:
                ls.append([int(i) for i in row])
        board = SilverToolBoard.from_board(ls, [px, py], [ex, ey])
        return board

    def quit(self):
        pygame.quit()
        exit()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.board.move_right()
        elif keys[pygame.K_LEFT]:
            self.board.move_left()
        elif keys[pygame.K_DOWN]:
            self.board.move_down()
        elif keys[pygame.K_UP]:
            self.board.move_up()

    def _save(self):
        with open(os.path.join('puzzles', 'tempSilver.csv'), mode='w', newline='') as f:
            px, py = self.board.player_pos
            ex, ey = self.board.win_pos
            writer = csv.writer(f)
            writer.writerow((px, py, ex, ey, self.board.width, self.board.height))
            writer.writerows([[int(i) for i in j] for j in self.board.board])

    def run(self):
        clock = pygame.time.Clock()
        self.board.resize_to_fit(self.screen)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._save()
                    self.quit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                    for btn in self.btns:
                        if not btn.collide_point(event.pos):
                            continue
                        for btn1 in self.btns:
                            btn1.active = False
                        btn.active = True
                        self.board.cur_placement = btn.id
                        break
                    else:
                        self.board.get_click(event.pos)
                        if self.exit.collide_point(event.pos):
                            self.quit()
            self.handle_input()
            self.screen.fill('black')
            self.board.render(self.screen)
            self.exit.render(self.screen)
            for btn in self.btns:
                btn.render(self.screen)
            pygame.display.flip()
            clock.tick(60)
