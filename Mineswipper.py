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
    tile_size = screen_size[0] / map_grid.size[0]
    return win


def set_image(img, img_size):
    img_sp = pygame.image.load(img).convert()
    img_sp.set_colorkey(BLACK)
    return pygame.transform.scale(img_sp, img_size)


# rects
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
red = pygame.color.Color.r  # correct?

score_dir = {}


pygame.init()
pygame.mixer.init()
pygame.display.set_caption('Mine')

mine_sp = pygame.sprite.Group()
# score_dir = {}
# path = os.path.join(os.getcwd(), 'img')  # path.dirname(__file__)
tiles = 10

# map
bombs = 20
map_emp = np.zeros(tiles ** 2)
map_emp[:bombs - 1] = np.ones(bombs)  # creates ones, count bomb
map_grid = np.random.shuffle(map_emp).reshape((tiles, tiles))  # random positions ofd ones
tile_size = 30  # todo add window div by x square

screen_size = map_grid.size * tile_size

fps = 30
# 3 cac just add 3 sprights
colors = []  # todo add cmap so more = red


def border(pos):
    # check if outside range
    # dont change pos just search
    s_range = pos
    for num in range(2):
        if 0 >= s_range[num]:
            s_range[num] = 1
        elif s_range[num] >= map_grid.size[num]:
            s_range[num] = map_grid.size[num] - 1

    # test
    search_arr = map_grid[(s_range[0] - 1):(s_range[0] + 1), (s_range[1] - 1):(s_range[1] + 1)]
    return sum(search_arr)


class Mine:
    def __init__(self, active, position):
        self.position = position  # place in grid
        self.bomb = active
        self.borders = border(self.position)
        self.image = ''
        # if self.bomb

    def text(self):
        font = pygame.font.Font('comicsans', 30)
        # location
        locat = self.position + tile_size / 2  # vector, but work:::center tect
        score_out = font.render(str(self.borders), True, WHITE)  # colors[self.borders]  # color of text fix so rgb

        text_rec = score_out.get_rect()
        text_rec.center = locat
        game.game_window.blit(score_out, text_rec)

    def click(self):
        if self.bomb:
            boom()
        else:
            self.image = ''  # texts.rend borders


def boom():
    # play boom, animation spiral out from mom show all boms
    # save time, go to menu
    # menu text input bom count, size
    pass


class Game:
    def __init__(self):
        self.game_window = update_window()
        # Clock object
        self.clock = pygame.time.Clock()
        self.time = 0
        self.state = 'alive'
        self.run = True

        self.restart()
        self.running()

    def level(self):  # level score?, run indie from level
        # removes old positions
        # play d sound
        self.run = False
        # self.g_over()
        self.restart()

        pass

    def menu(self):
        button_ls = ['quit', 'easy', 'medium', 'hard']
        # create button
        len_b = len(button_ls)
        screen_pos = (screen_size[1] - 40) / len_b

        for b in range(len_b):
            but_pos = (10 + screen_pos) * b
            rec = pygame.Surface((50, but_pos))
            rec.fill(BLUE)

            text_surf = pygame.font.Font('freesansbold.ttf', 30).render(button_ls[b], True, WHITE)
            self.game_window.blit(text_surf, rec)

        # todo add coustom then call grid

        # start = True
        # qui = False  # menu
        # if start:
        #     self.restart()
        # elif qui:
        #     self.quit()
    def events(self):
        global screen_size
        for event in pygame.event.get():
            print(event, event.type)
            if event.type == pygame.QUIT:
                self.run = False  # breaks loop
                game_quit()

            elif event.type == VIDEORESIZE:
                width, height = event.size
                height = width / 2
                screen_size = (int(width), int(height))

                # # max dim
                # size_fact = max(size)
                # size_ind = size.index(size_fact)  # so we can
                self.game_window = update_window()
            elif event.type == MOUSEBUTTONDOWN:  # only looks when pressed
                mouse_pos = pygame.mouse.get_pos()
                tile_index = np.array(mouse_pos) / tile_size  # gets tile index of button
                map_grid[tile_index].click()  # dous click on bomb in pos

    def running(self):
        while self.run:
            self.clock.tick(fps)

            if self.state == 'alive':
                # todo level end map
                self.level()
            elif self.state == 'menu':
                self.menu()
            # pause
            self.game_window.fill(BLACK)

            self.time += self.clock.get_time()
            # play background
            self.score()  # calls score function
            pygame.display.flip()

    def draw_lines(self):
        for i in range(map_grid.size[0]):  # x values same each
            # draw line on x, y = 0:width and same for y, x = 0:width. incrementing for number of lines see above
            pygame.draw.line(self.game_window, (255, 255, 255), (tile_size * i, 0), (tile_size * i, screen_size[0]))
            pygame.draw.line(self.game_window, (255, 255, 255), (0, tile_size * i), (screen_size[0], tile_size * i))

            # line = pygame(line) all op vall and cur pos is pix_size*i
            # scren blit

    def restart(self):
        # Clock object
        self.clock = pygame.time.Clock()
        self.time = 0
        # countdown
        # player stand

    # def g_over(self):
    #     """get score end loop, get time return ask is replay"""
    #     self.menu(score=self.total_score, de=True)

    def score(self):
        font = pygame.font.Font('freesansbold.ttf', 30)
        # time = 0  # placehold
        # location
        text_x = 100  # screen_size - pix_per_caract(fsize)*len
        text_y = 10
        score_out = font.render("Time: " + str(self.time), True, WHITE)
        text_rec = score_out.get_rect()
        text_rec.midtop = (text_x, text_y)
        self.game_window.blit(score_out, text_rec)

    def save_score(self):
        # ask text
        na = input('name: ')  # todo fix so input text
        with open(na + f'_time_{bombs}.txt', 'w') as fi:
            fi.write(str(self.time))


def game_quit():
    pygame.quit()
    sys.exit()


game = Game()
