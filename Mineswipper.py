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


def update_window():
    global tile_size, screen_size
    win = pygame.display.set_mode(screen_size, pygame.RESIZABLE)

    # todo add to loop
    screen_size = win.get_size()  # redefine screen_size in loop
    tile_size = int(screen_size[0] / map_grid.shape[0])
    return win


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

tiles = 10


# map
bombs = 20
map_grid = np.zeros(tiles ** 2)
map_grid[:bombs] = np.ones(bombs)  # creates ones, count bomb
np.random.shuffle(map_grid)  #
map_grid = map_grid.reshape(tiles, tiles)  # random positions ofd ones

mine_sp = pygame.sprite.Group()
but_sp = pygame.sprite.Group()
expl_sp = pygame.sprite.Group()

tile_size = 30  # todo add window div by x square

screen_shape = np.array(map_grid.shape)
screen_shape = np.flip(screen_shape)
screen_shape[1] += 1  # se
screen_size = screen_shape * tile_size

fps = 30
# 3 cac just add 3 sprights
colors = []  # todo add cmap so more = red

explosion = pygame.mixer.Sound(os.path.join(path, 'Explosion.wav'))


def set_image(img, pat=path):
    img_p = os.path.join(pat, img)

    img_sp = pygame.image.load(img_p).convert()
    return pygame.transform.scale(img_sp, (tile_size, tile_size))


def border(pos, grid=map_grid):
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


def create_mines():
    mine_ls = []
    for row in range(map_grid.shape[0]):  # loop numpers
        for col in range(map_grid.shape[1]):
            mine_obj = Mine(map_grid[row, col], (row, col))  # position xy, active m,g[x,y]
            mine_ls.append(mine_obj)

    return np.array(mine_ls).reshape(map_grid.shape)


def flood_fill(mine_h):  # search
    # x = game.mine_map[1, 2]
    if not mine_h.bomb and not mine_h.open:  # only clicks on not bombs, returns if already
        mine_h.open = True  # ie checked
        bord = border(mine_h.position, game.mine_map)
        # print(bord)
        print(mine_h.borders, mine_h.position)
        if mine_h.borders == 0:
            for mi_row in bord:
                for mi in mi_row:
                    mi.click('1')  # only loops though spaces if not touch, spaces openm by click, no chance of explos
                    # they will then send back ie recursive boms surround


def boom():
    # play boom, animation spiral out from mom show all boms
    # save time, go to menu
    # menu text input bom count, size
    # print line scan,
    li = 5
    # wait line
    # result = np.where(arr == 15)
    print('booooooooooom')
    game.level_over()

    # for mi in game.mine_map[li, :]:
    #     mi.click('1', act=False)  # maybe not clic, just empty, if first change bomb to red


class Explosion(pygame.sprite.Sprite):
    def __init__(self, position):
        super(Explosion, self).__init__()
        self.position = position
        self.img_ind = 0

        self.image_ls = [set_image(x, ex_path) for x in os.listdir(ex_path)
                         if x.endswith('.png')]

        self.image = self.image_ls[self.img_ind]
        self.rect = self.image.get_rect()
        self.rect.topleft = np.flip(self.position) * tile_size

    def update(self):
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect.topleft = np.flip(self.position) * tile_size

        self.img_ind = (self.img_ind + 1) % len(self.image_ls)
        self.image = self.image_ls[self.img_ind]


class Mine(pygame.sprite.Sprite):
    def __init__(self, active, position):
        super(Mine, self).__init__()

        # images
        self.img_pre = 'minesweeper_tiles '
        self.image = set_image('minesweeper_tiles plain.jpg')

        # positions
        self.bomb = active
        self.position = position  # place in grid
        self.borders = int(np.sum(border(self.position)))

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
                boom()

        else:
            flood_fill(self)
            self.image = set_image(f'minesweeper_tiles {self.borders}.jpg')  # image with correct borders

    def expl(self):
        explosion.play()
        w, h = self.image.get_size()
        for x in range(w):
            for y in range(h):
                color = self.image.get_at((x, y))  # darkens color
                color = [max(0, c) for c in color[:-1]] + [color[-1]]
                self.image.set_at((x, y), pygame.Color(color))


class Button(pygame.sprite.Sprite):
    def __init__(self, position, name):
        super(Button, self).__init__()
        self.name = name
        self.size = (5, 1)  # (screen_size[0] // 2, int(but_pos * tile_size))
        self.pos = position

        self.image = pygame.Surface(np.array(self.size) * tile_size)  # 5, 1 button
        self.image.fill(BLUE)

        self.rect = self.image.get_rect()
        self.rect.center = self.pos  # (screen_size[0] / 2,

        text_surf = pygame.font.Font('freesansbold.ttf', 15).render(self.name, True, WHITE)
        text_rect = text_surf.get_rect()
        text_rect.center = self.rect.center  # center text
        self.image.blit(text_surf, text_rect)


class Game:
    def __init__(self):
        self.game_window = update_window()
        # Clock object
        self.clock = pygame.time.Clock()
        self.time = 0
        self.state = 'menu'
        self.run = True
        self.mine_num = 20  # add change

        self.mine_map = create_mines()

    def create_mines(self, map_grid):
        mine_ls = []
        for row in range(map_grid.shape[0]):  # loop numpers
            for col in range(map_grid.shape[1]):
                mine_obj = Mine(map_grid[row, col], (row, col))  # position xy, active m,g[x,y]
                mine_ls.append(mine_obj)

        return np.array(mine_ls).reshape(map_grid.shape)

    def exploion(self, dt, pos):
        rad = 0.5 * dt  # dis
        x_range = np.arrage(-rad, rad, 0.5) + pos[0]
        y_range = np.sqrt(rad ** 2 - x_range ** 2) + pos[1]
        for x, y in zip(x_range, y_range):
            curr_mine = self.mine_map[x, int(y)]
            if curr_mine.bomb:
                pass

        # initial pos
    def menu(self):
        button_ls = ['quit', 'easy', 'medium', 'hard']
        # create button
        len_b = len(button_ls)
        # screen_pos = (screen_size[1] - 40) / len_b
        but_p_tile = (self.mine_map.shape[0] - 2) / len_b   # rows

        for b in range(len_b):
            but_pos = but_p_tile * b + 1
            button = pygame.Surface((tile_size * 5, tile_size))  # 5, 1 button
            button.fill(BLUE)
            but_rect = button.get_rect()
            but_rect.center = (screen_size[0] // 2, int(but_pos * tile_size))

            text_surf = pygame.font.Font('freesansbold.ttf', 15).render(button_ls[b], True, WHITE)
            text_rect = text_surf.get_rect()
            text_rect.center = but_rect.center  # center text
            self.game_window.blit(button, but_rect)
            self.game_window.blit(text_surf, text_rect)  # after so shows on top

        # todo add coustom then call grid

        #     game.quit()
    def events(self):
        global screen_size
        for event in pygame.event.get():
            # print(event, event.type)
            if event.type == pygame.QUIT:
                self.run = False  # breaks loop
                game_quit()

            elif event.type == VIDEORESIZE:
                width, height = event.size
                height = width + 1
                screen_size = (int(width), int(height))

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
                            print('re')
                            self.restart()
                        elif but.name == 'med':
                            pass
                        elif but.name == 'hard':
                            pass
                        elif but.name == 'coustom':
                            pass
                    pass
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
            self.game_window.fill(BLACK)
            mine_sp.draw(self.game_window)

            self.clock.tick(fps)
            self.events()
            if self.state == 'alive':
                # todo level end map
                self.level_over()
            elif self.state == 'menu':
                self.menu()
            # pause

            # self.draw_lines()
            self.time += self.clock.get_time()
            # play background
            self.score()  # calls score function
            pygame.display.flip()

    def draw_lines(self):
        for n, si in enumerate(map_grid.shape):  # x, y
            for i in range(si):  # x values same each
                end = [tile_size * i, screen_size[n]]
                st = [tile_size * i, 0]
                if n:
                    st.reverse()
                    end.reverse()
                # draw line on x, y = 0:width and same for y, x = 0:width. incrementing for number of lines see above
                pygame.draw.line(self.game_window, WHITE, st, end)

            # line = pygame(line) all op vall and cur pos is pix_size*i
            # scren blit

    def restart(self, cnt=20, til=100):
        # Clock object
        self.clock = pygame.time.Clock()
        self.time = 0  # wait till start

        self.mine_num = cnt

        # map
        map_grid = np.zeros(til ** 2)
        map_grid[:cnt] = np.ones(bombs)  # creates ones, count bomb
        np.random.shuffle(map_grid)  #
        self.map_grid = self.create_mines(map_grid.reshape(til, til))  # random positions ofd ones

        # creat mines based on user size
        # countdown
        # player stand

    def level_over(self, clear_bord=False):  # level score?, run indie from level
        if clear_bord:
            print('save_score')
        else:
            print('dead')
            self.menu()
        # removes old positions
        # play d sound
        # game.run = False
        # # game.g_over()
        # game.restart()

    # def g_over(game):
    #     """get score end loop, get time return ask is replay"""
    #     game.menu(score=game.total_score, de=True)

    # self.restart()
    # self.running()

    def score(self):
        # gui
        gui_surf = pygame.Surface((screen_size[0], tile_size))
        gui_surf.fill(BLUE)
        gui_rect = gui_surf.get_rect()
        gui_rect.bottomleft = (0, screen_size[1])  # bottom left in b/left screen

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
        mine_rect.midright = (screen_size[0], gui_rect.center[1])  # mid y, far right

        # blit
        self.game_window.blit(gui_surf, gui_rect)
        self.game_window.blit(score_out, text_rec)
        self.game_window.blit(mine_gui, mine_rect)

    def save_score(self):
        # ask text
        na = input('name: ')  # todo fix so input text
        with open(na + f'_time_{bombs}.txt', 'w') as fi:
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

            print(m)
            print()
            print()

        print('bord state')
        loop(np.zeros(self.mine_map.shape, int).astype('str'))
        loop(np.zeros(self.mine_map.shape, int).astype('str'), True)


def game_quit():
    pygame.quit()
    sys.exit()


game = Game()
game.running()
