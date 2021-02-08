import pygame
import numpy as np
from pygame.locals import *
import os
import sys


# rects
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
red = pygame.color.Color.r  # correct?

score_dir = {}


pygame.init()
pygame.mixer.init()

pygame.display.set_caption('Mine')

# score_dir = {}
path = os.path.join(os.path.dirname(__file__), 'img', 'mines')
ex_path = os.path.join(path, 'Explosions_kenney')

# map
# bombs = 20
# map_grid = np.zeros(tiles ** 2)
# map_grid[:bombs] = np.ones(bombs)  # creates ones, count bomb
# np.random.shuffle(map_grid)  #
# map_grid = map_grid.reshape(tiles, tiles)  # random positions ofd ones

mine_sp = pygame.sprite.Group()
but_sp = pygame.sprite.Group()
expl_sp = pygame.sprite.Group()

tile_size = 30

fps = 30
# 3 cac just add 3 sprights

explosion = pygame.mixer.Sound(os.path.join(path, 'Explosion.wav'))


class Button(pygame.sprite.Sprite):
    def __init__(self, position, name):
        super(Button, self).__init__()
        self.name = name
        self.size = (6, 2)  #
        self.pos = (game.screen_size[0] // 2, int(position * tile_size))

        self.image = pygame.Surface(np.array(self.size) * tile_size)  # 5, 1 button
        self.image.fill(BLUE)

        self.rect = self.image.get_rect()
        self.rect.midtop = self.pos  # (screen_size[0] / 2,

        text_surf = pygame.font.Font('freesansbold.ttf', 10).render(self.name, True, WHITE)
        text_rect = text_surf.get_rect()
        # text_rect.center = self.rect.center  # center text
        self.image.blit(text_surf, text_rect)
        but_sp.add(self)

class Game:
    def __init__(self):

        # Clock object
        self.clock = pygame.time.Clock()
        self.time = 0
        self.last_loop = pygame.time.get_ticks()
        self.state = 'menust'

        self.run = True
        self.mine_num = 20  # add change

        self.tile_cnt = 10
        self.map_grid = np.zeros(self.tile_cnt ** 2).reshape((self.tile_cnt, self.tile_cnt))
        self.mine_map = None  # None

        self.dt = 0
        self.active_local = (0, 0)

        screen_shape = np.array(self.map_grid.shape)
        screen_shape = np.flip(screen_shape)
        screen_shape[1] += 1  # se

        screen_size = screen_shape * tile_size

        self.game_window = pygame.display.set_mode(screen_size, pygame.RESIZABLE)

        self.screen_size = self.game_window.get_size()  # redefine screen_size in loop
        self.tile_size = int(screen_size[0] / self.map_grid.shape[0])


    def menu(self):
        self.state = 'menu'
        button_ls = ['quit']  # , 'easy', 'medium', 'hard']
        # create button
        len_b = len(button_ls)
        # screen_pos = (screen_size[1] - 40) / len_b
        but_p_tile = (self.mine_map.shape[0] - 2) / len_b   # rows

        for b in range(len_b):
            but_pos = but_p_tile * b + 1
            Button(but_pos, button_ls[b])

        # todo add coustom then call grid

        #     game.quit()

    # noinspection PyUnresolvedReferences
    def events(self):
        for event in pygame.event.get():
            # print(event, event.type)
            if event.type == pygame.QUIT:
                self.run = False  # breaks loop
                game_quit()

            elif event.type == VIDEORESIZE:
                width, height = event.size
                height = width + 1
                self.screen_size = (int(width), int(height))

                # # max dim
                # size_fact = max(size)
                # size_ind = size.index(size_fact)  # so we can
                self.game_window = update_window()
            elif event.type == MOUSEBUTTONDOWN:  # only looks when pressed
                mouse_pos = pygame.mouse.get_pos()
                if self.state == 'menu':  # diff index
                    mouse_sp = pygame.sprite.Sprite()
                    mouse_sp.rect = pygame.Rect(mouse_pos[0], mouse_pos[1], 1, 1)  # mouse sprite 1,1 rext

                    col_ls = pygame.sprite.spritecollide(mouse_sp, but_sp, False)  # check if mouse hit
                    if col_ls:
                        but_sp.empty()  # removes all
                    print(col_ls)
                    for but in col_ls:  # test collision
                        if but.name == 'quit':
                            game_quit()
                        elif but.name == 'easy':  # or but.name == 'restart':
                            self.tile_cnt = 10
                            self.mine_num = 20

                        elif but.name == 'med':
                            self.tile_cnt = 15
                            self.mine_num = 50

                        elif but.name == 'hard':
                            self.tile_cnt = 20
                            self.mine_num = 100

                        elif but.name == 'coustom':
                            pass
                        but_sp.empty()
                        self.restart()

                else:
                    tile_index = np.array(mouse_pos) // tile_size  # gets tile index of button
                    tile_index = np.flip(tile_index)
                    if all(map(lambda x, y: x < y, tile_index, self.mine_map.shape)):  # if in bouds do else ignore
                        mi = self.mine_map[tile_index[0], tile_index[1]]
                        # for x in mi:
                        mi.click(event.button)  # dous click on bomb in pos
                        self.print_board()

    def running(self):
        while self.run:
            mine_sp.update()
            but_sp.update()
            self.game_window.fill(BLACK)

            but_sp.draw(self.game_window)
            self.clock.tick(fps)
            self.events()

            if self.state == 'menust':
                self.menu()
                print(but_sp)

            else:
                # self.draw_lines()
                self.time += self.clock.get_time()
                # play background
            pygame.display.flip()

    def restart(self):
        # Clock object
        self.clock = pygame.time.Clock()
        self.time = 0  # wait till start
        self.dt = 0

        but_sp.empty()
        expl_sp.empty()
        mine_sp.empty()

        self.last_loop = pygame.time.get_ticks()
        self.state = 'me'

        # map
        self.map_grid = np.zeros(self.tile_cnt ** 2)
        self.map_grid[:self.mine_num] = np.ones(self.mine_num)  # creates ones, count bomb
        np.random.shuffle(self.map_grid)  #
        self.map_grid = self.map_grid.reshape(self.tile_cnt, self.tile_cnt)
        self.mine_map = self.map_grid

    def level_over(self, clear_bord=False):  # level score?, run indie from level
        self.state = 'menust'
        self.time = 0  # wait till start
        self.dt = 0
        self.mine_num = 0
        # clear sp

        if clear_bord:
            print('save_score')
            self.save_score()
        else:
            print('dead')
            self.menu()  # todo restart?

    def score(self):
        # gui
        gui_surf = pygame.Surface((self.screen_size[0], tile_size))
        gui_surf.fill(BLUE)
        gui_rect = gui_surf.get_rect()
        gui_rect.bottomleft = (0, self.screen_size[1])  # bottom left in b/left screen

        font = pygame.font.Font('freesansbold.ttf', 10)

        # text time
        score_out = font.render("Time: " + str(int(self.time / 1000)), True, WHITE)
        text_rec = score_out.get_rect()
        text_rec.center = gui_rect.center

        # text num mines:  will get passed 0 for all empty spaces and 1 for active, if flag, not passed anything
        true_active = self.mine_num
        estimated_active = 0
        for mi in self.mine_map.flatten():
            if mi.bomb and mi.flag:  # player is correct so tot can be rem
                true_active -= 1
            elif mi.bomb:  # already taken into acount above, since both cancle
                estimated_active += 1
            elif mi.flag:  # cant be both sice top doesnt matter if put on wrong space, still counts correct
                estimated_active -= 1

        if true_active == 0:  # no b left win
            self.level_over(True)

        mine_gui = font.render("Mines: " + str(int(estimated_active)), True, WHITE)

        mine_rect = mine_gui.get_rect()
        mine_rect.midright = (self.screen_size[0], gui_rect.center[1])  # mid y, far right

        # blit
        self.game_window.blit(gui_surf, gui_rect)
        self.game_window.blit(score_out, text_rec)
        self.game_window.blit(mine_gui, mine_rect)

    def save_score(self):
        # ask text
        na = input('name: ')  # todo fix so input text
        with open(na + f'_time_{self.mine_num}.txt', 'w') as fi:
            fi.write(str(self.time))

    def print_board(self):
        def loop(m, open_x=False):
            def check():
                if self.mine_map[row, col].bomb:
                    m[row, col] = 'x'
                else:
                    m[row, col] = self.mine_map[row, col].borders
            for row in range(m.shape[0]):
                for col in range(m.shape[1]):
                    if open_x:
                        if self.mine_map[row, col].clicked:
                            check()
                    else:
                        check()

            # print(m)
            # print()
            # print()

        print('bord state')
        loop(np.zeros(self.mine_map.shape, int).astype('str'))
        loop(np.zeros(self.mine_map.shape, int).astype('str'), True)

    def update_window(self):
        self.game_window = pygame.display.set_mode(self.screen_size, pygame.RESIZABLE)

        self.screen_size = self.game_window.get_size()  # redefine screen_size in loop
        self.tile_size = int(self.screen_size[0] / self.map_grid.shape[0])


def game_quit():
    pygame.quit()
    sys.exit()


game = Game()
game.restart()
game.state = 'menust'
game.running()