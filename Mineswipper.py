import pygame
import numpy as np
from pygame.locals import *
import os
import sys


def get_high():
    for sc in os.listdir('HighScores'):
        na = sc.replace('_score.txt', '')
        with open(sc) as fi:
            score_dir[na] = fi.read()


# rects
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
red = pygame.color.Color.r  # correct?
but_col = (0, 0, 255)
but_col_clicked = (50, 0, 200)
gui_col = (20, 0, 230)

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
click_sp = pygame.sprite.Group()
tile_size = 30

fps = 30
# 3 cac just add 3 sprights

explosion = pygame.mixer.Sound(os.path.join(path, 'Explosion.wav'))


def set_image(img, pat=path):
    img_p = os.path.join(pat, img)

    img_sp = pygame.image.load(img_p).convert()
    return pygame.transform.scale(img_sp, (tile_size, tile_size))


def flood_fill(mine_h):  # search
    # x = game.mine_map[1, 2]
    if not mine_h.bomb and not mine_h.open:  # only clicks on not bombs, returns if already
        mine_h.open = True  # ie checked
        bord = game.border(mine_h.position, game.mine_map)
        # print(bord)
        print(mine_h.borders, mine_h.position)
        if mine_h.borders == 0:
            for mi_row in bord:
                for mi in mi_row:
                    mi.click('1')  # only loops though spaces if not touch, spaces openm by click, no chance of explos
                    # they will then send back ie recursive boms surround


class MineBoard:
    def __init__(self, size, block_size):
        self.board = np.array((size, size))
        pass


class Explosion(pygame.sprite.Sprite):
    def __init__(self, position):
        super(Explosion, self).__init__()
        self.position = position
        self.img_ind = 0

        self.image_ls = [set_image(x, ex_path) for x in os.listdir(ex_path)
                         if x.endswith('.png')]

        self.image = self.image_ls[self.img_ind]
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        expl_sp.add(self)

    def update(self):
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect.topleft = np.flip(self.position) * tile_size

        self.img_ind = (self.img_ind + 1) % len(self.image_ls)
        self.image = self.image_ls[self.img_ind]
        # todo rm percent then if ind = len, clear from group


class Mine(pygame.sprite.Sprite):
    def __init__(self, active, position):
        super(Mine, self).__init__()

        # images
        self.img_pre = 'minesweeper_tiles '
        self.image = set_image('minesweeper_tiles plain.jpg')

        # positions
        self.bomb = active
        self.position = position  # place in grid
        self.borders = int(np.sum(game.border(self.position)))

        # rects
        self.rect = self.image.get_rect()
        self.rect.topleft = np.flip(self.position) * tile_size

        # test values
        self.clicked = False
        self.flag = False
        self.open = False  # floodfill
        mine_sp.add(self)
        # if game.bomb

    def text(self):
        font = pygame.font.Font('comicsans', 30)
        # location
        locat = self.position + tile_size / 2  # vector, but work:::center tect
        score_out = font.render(str(self.borders), True, WHITE)  # colors[game.borders]  # color of text fix so rgb

        text_rec = score_out.get_rect()
        text_rec.center = locat
        game.game_window.blit(score_out, text_rec)

    def update(self):
        # size of all images
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect.topleft = np.flip(self.position) * tile_size
        pass

    def click(self, button, act=True):
        self.clicked = True
        if button == 3:  # right click
            if self.flag:  # inverts
                self.image = set_image('minesweeper_tiles plain.jpg')
                self.flag = False

            else:
                self.flag = True
                self.image = set_image('minesweeper_tiles flag.jpg')  # flag, b/left -1

        elif self.bomb and not self.flag:  # no click on flag
            self.image = set_image('minesweeper_tiles mine.jpg')
            if act:  # prevents recursive
                game.boom(self.position)

        else:
            flood_fill(self)
            self.image = set_image(f'minesweeper_tiles {self.borders}.jpg')  # image with correct borders

    def expl(self):
        explosion.play()
        self.clicked = True
        w, h = self.image.get_size()
        Explosion(self.rect.center)
        for x in range(w):
            for y in range(h):
                color = self.image.get_at((x, y))  # darkens color
                alph = color.a  # last index
                color = [max(0, c - 50) for c in color[:-1]]
                color.append(alph)
                self.image.set_at((x, y), pygame.Color(color))


class Button(pygame.sprite.Sprite):
    def __init__(self, position, name):  # active if text
        super(Button, self).__init__()
        self.name = name
        self.size = (5, 1)  #
        self.active = False
        if self.name == 'save_score' or self.name == 'custom':
            self.active = True
        self.clicked = False
        self.pos = (game.screen_size[0] // 2, int(position * tile_size))

        self.image = pygame.Surface(np.array(self.size) * tile_size)  # 5, 1 button

        self.color = but_col if self.active else gui_col
        self.text = self.name
        self.image.fill(BLUE)

        self.rect = self.image.get_rect()
        self.rect.midtop = self.pos  # (screen_size[0] / 2,

        text_surf = pygame.font.Font('freesansbold.ttf', 10).render(self.text, True, WHITE)
        text_rect = text_surf.get_rect()
        text_rect.center = np.array(self.rect.size) // 2  # center text
        self.image.blit(text_surf, text_rect)
        but_sp.add(self)
        if self.active:
            click_sp.add(self)

    def input_text(self, event):
        print('x')
        if not self.clicked:
            self.color = but_col
        else:
            self.color = but_col_clicked

            if event.type == pygame.KEYDOWN:  # test key
                if event.key == pygame.K_RETURN:
                    string = self.text
                    self.text = self.name
                    return string
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode  # clears input on enter, removes car on back and adds else
        return None

    def update(self):
        text_surf = pygame.font.Font('freesansbold.ttf', 10).render(self.text, True, WHITE)
        self.image.fill(self.color)
        text_rect = text_surf.get_rect()
        text_rect.center = np.array(self.rect.size) // 2  # center text
        self.image.blit(text_surf, text_rect)


class Game:
    def __init__(self):

        # Clock object
        self.clock = pygame.time.Clock()
        self.time = 0
        self.last_loop = pygame.time.get_ticks()
        self.state = 'menust'

        self.run = True
        self.input = False
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
        self.button_ls = ['quit', 'easy', 'medium', 'hard', 'custom']

    def create_mines(self):
        mine_ls = []
        for row in range(self.map_grid.shape[0]):  # loop numpers
            for col in range(self.map_grid.shape[1]):
                mine_obj = Mine(self.map_grid[row, col], (row, col))  # position xy, active m,g[x,y]
                mine_ls.append(mine_obj)

        return np.array(mine_ls).reshape(self.map_grid.shape)

    def border(self, pos, grid=None):
        if grid is None:
            grid = self.map_grid
        # check if outside range
        # dont change pos just search
        search_op = []
        for num in range(2):
            min_val = max([0, pos[num] - 1])
            up_val = min([pos[num] + 1, grid.shape[num] - 1])
            search_op.append([min_val, up_val + 1])

        # test
        search_arr = grid[search_op[0][0]:search_op[0][1], search_op[1][0]:search_op[1][1]]
        return search_arr

    def boom(self, pos):
        self.state = 'ex'
        self.active_local = pos

    def exploion(self):  # todo update screen
        rad = self.dt  # dismove 1 ev frame

        x_range = np.arange(-rad, rad, 0.1)  # sice rad - issue
        for x in x_range:

            y_abs = np.sqrt(rad ** 2 - x ** 2)
            x = int(x) + self.active_local[0]
            ya = np.array([-y_abs, y_abs]) + self.active_local[1]
            for y in ya:
                y = int(y)
                print(x, y)
                if 0 < x < self.mine_map.shape[0] and 0 < y < self.mine_map.shape[1]:

                    curr_mine = self.mine_map[x, y]
                    curr_mine.image = set_image('minesweeper_tiles mine.jpg')
                    # if curr_mine.bomb and not curr_mine.clicked:
                    #     print('exp')
                    #     curr_mine.expl()

        if all(m.clicked for m in self.mine_map.flatten()):  # all bombs
            self.level_over()

    def menu(self):
        self.state = 'menu'

        # create button
        len_b = len(self.button_ls)
        # screen_pos = (screen_size[1] - 40) / len_b
        but_p_tile = (self.mine_map.shape[0] - 2) / len_b   # rows

        for b in range(len_b):
            but_pos = but_p_tile * b + 1
            Button(but_pos, self.button_ls[b])

        # todo add coustom then call grid

        #     game.quit()

    # noinspection PyUnresolvedReferences
    def events(self):
        for event in pygame.event.get():
            if self.input:
                ret_st = {but.name: but.input_text(event) for but in click_sp}  # get only one line and update,
                # todo only do if no vals, todo active list
                print(ret_st)
                if ret_st.values():
                    if 'save_score' in ret_st.keys() and ret_st['save_score']:  # check if val
                        self.save_score(ret_st['save_score'])
                    elif 'custom' in ret_st.keys() and ret_st['custom']:
                        self.tile_cnt, self.mine_num = ret_st['custom'].split(',')

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
                self.update_window()
            elif event.type == MOUSEBUTTONDOWN:  # only looks when pressed
                mouse_pos = pygame.mouse.get_pos()
                if self.state == 'menu':  # diff index
                    mouse_sp = pygame.sprite.Sprite()
                    mouse_sp.rect = pygame.Rect(mouse_pos[0], mouse_pos[1], 1, 1)  # mouse sprite 1,1 rext

                    active_col = pygame.sprite.spritecollide(mouse_sp, click_sp, False)
                    if active_col:
                        self.input = not self.input
                        for but in click_sp:
                            if but not in active_col:
                                but.clicked = False
                            else:
                                but.text = ''
                                but.clicked = not but.clicked
                    else:
                        col_ls = pygame.sprite.spritecollide(mouse_sp, but_sp, False)  # check if mouse hit

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

            mine_sp.draw(self.game_window)
            but_sp.draw(self.game_window)
            expl_sp.draw(self.game_window)

            self.clock.tick(fps)
            self.events()

            if self.state == 'menust':
                self.menu()
                print(but_sp)
            elif self.state == 'ex':
                now = pygame.time.get_ticks()
                if now - self.last_loop > 200:
                    self.dt += 1
                    self.last_loop = now
                    self.exploion()
                    # pause
            else:
                # self.draw_lines()
                self.time += self.clock.get_time()
                # play background
                self.score()  # calls score function
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
        self.mine_map = self.create_mines()  # random positions ofd ones

    def level_over(self, clear_bord=False):  # level score?, run indie from level
        self.state = 'menust'
        self.time = 0  # wait till start
        self.dt = 0
        self.mine_num = 0
        # clear sp

        if clear_bord:
            self.button_ls.append('save_score')

            print('save_score')
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

    def save_score(self, na):
        # ask text
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
