import pygame
from pygame.locals import *
import random
import numpy as np
import os
import sys



def meters_to_pixels(met):
    def met_con(x):
        return round(pix_per_met * x)
    if type(met) is tuple:
        pix = tuple(map(met_con, met))
    else:
        pix = met_con(met)
    return pix


def get_high():
    for sc in os.listdir('HighScores'):
        na = sc.replace('_score.txt', '')
        with open(sc) as fi:
            score_dir[na] = fi.read()


pygame.init()
pygame.mixer.init()
pygame.display.set_caption('Dino')

score_dir = {}
path = os.path.join(os.getcwd(), 'img')  # path.dirname(__file__)
screen_size_meters = (30, 15)

time_mod = 5  # for time
time_multiple = 1
fps = 30  # def mov as pixx/s, m/s and pix/f
speed = 10

f_rate = 30
pix_per_met = 50
screen_size = tuple(map(meters_to_pixels, screen_size_meters))  # (60, 30)  #
enemies = ['trip', 'cactus', 'bird']  # 1,3: low, high def in object or at rand... change prob?
# 3 cac just add 3 sprights

# din not image, path
d_path = os.path.join(path, 'p1_walk')

cac_img = os.path.join(path, 'p2_stand.png')
bird_img = os.path.join(path, 'enemyRed3.png')
back_img = os.path.join(path, 'planet_3_0.png')


# rects
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
red = pygame.color.Color.r  # correct?

sprites = pygame.sprite.Group()  # list all sps
enemy_sp = pygame.sprite.Group()
but_sp = pygame.sprite.Group()

vel_fr = meters_to_pixels(speed) / 30  # m/s


def update_window():
    global pix_per_met, screen_size
    win = pygame.display.set_mode(screen_size, pygame.RESIZABLE)

    # todo add to loop
    screen_size = win.get_size()  # redefine screen_size in loop
    pix_per_met = screen_size[0] / screen_size_meters[0]
    return win


def set_image(img, img_size):
    img_sp = pygame.image.load(img).convert()
    img_sp.set_colorkey(BLACK)
    return pygame.transform.scale(img_sp, img_size)


def set_text(size):
    pass


class Dino(pygame.sprite.Sprite):
    def __init__(self):
        super(Dino, self).__init__()

        self.img_index = 0
        self.lives = 2
        self.size = meters_to_pixels((1, 2))
        self.app_size = (1, 2)  # change when duct

        # image
        # on init stand; on jump jump, on walk loop
        img_ls = ['stand', 'jump', 'hurt', 'duck']

        self.image_dir = {x: set_image(os.path.join(path, f'p1_{x}.png'), self.size) for x in img_ls}
        self.walk_images = [set_image(os.path.join(d_path, x), self.size)
                            for x in os.listdir(d_path) if x.endswith('.png')]

        self.image = self.image_dir['stand']
        self.rect = self.image.get_rect()

        # set pos
        self.pos = np.array(screen_size) //2
        self.rect.center = self.pos  # bottom on ground mid x
        self.air = False
        self.duck = False
        self.vel = 0

        self.v_jump = -10  # m/2 at jump
        sprites.add(self)

    def update_size(self):
        self.size = meters_to_pixels(self.app_size)
        for x, y in self.image_dir.items():
            self.image_dir[x] = pygame.transform.scale(y, tuple(self.size))

        self.image = self.image_dir['stand']  # fix, same separate init so lives are indie
        self.walk_images = [pygame.transform.scale(x, tuple(self.size)) for x in self.walk_images]
        # from standing and other stuff that resets ev death

        self.rect = self.image.get_rect()
        # set pos
        self.rect.midbottom = self.pos  # bottom on ground mid x

    def jump(self):  # maybe add qualifier @... for all
        keys = pygame.key.get_pressed()
        # if keys[pygame.K_ESCAPE]:  # check if true always?
        #     menu(sc=level_score)

        if self.duck and not (keys[pygame.K_DOWN] or keys[pygame.K_c]):
            print('up')
            self.app_size = (1, 2)
            self.duck = False
            self.image = self.image_dir['stand']
            self.rect = self.image.get_rect()
            self.rect.midbottom = self.pos

        elif not self.duck and (keys[pygame.K_DOWN] or keys[pygame.K_c]):
            self.app_size = (2, 1)  # todo filip
            self.image = pygame.transform.rotate(self.image_dir['duck'], -90)
            print('duck')

            cent = self.rect.center
            self.rect = self.image.get_rect()

            self.rect.center = cent  #
            # di = self.__dict__
            # print(di)
            # print(di['image'], di['rect'])
            self.duck = True

    def update(self):
        self.pos[0] += 1
        # def update, then check jump
        # jump only works on groun

        # else:  # either change v0 or take t from start .. put in otherloop, so just loop in air?
        #     dt = 1 / fps  # cloc.tick...ms since last t - t0  # t0 time at start, then
        #     self.rect.bottom += meters_to_pixels(self.vel * dt + 4.9 * dt ** 2)
        #     self.vel += 9.81 * dt
        #     # print('{}, {}'.format(game.rect.bottom, game.vel))
        #     if self.rect.bottom >= screen_size[1]:  # y/x?
        #         self.air = False
        #         self.rect.bottom = screen_size[1]
        pass

class Game:
    def __init__(self):
        global time_multiple

        self.total_score = 0
        self.level_score = 0
        self.level_num = 0

        # Clock object
        self.game_window = update_window()

        self.clock = pygame.time.Clock()
        self.back_sp = pygame.image.load(back_img).convert()

        self.time = 0
        self.state = 'menu'
        self.run = True
        self.dino = Dino()

        # game.restart()
        self.running()

    def events(self):
        global screen_size
        for event in pygame.event.get():
            # print(event, event.type)
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
                self.dino.update_size()

    def running(self):
        global screen_size
        while self.run:
            sprites.update()
            self.time += self.clock.get_time()

            self.game_window.fill(BLACK)
            self.game_window.blit(pygame.transform.scale(self.back_sp, screen_size), (0, 0))
            self.clock.tick(fps)
            self.events()
            # pause

            for b in but_sp:
                self.game_window.blit(b.image, b.rect)
            sprites.draw(self.game_window)

            self.level_score = self.time
            # play background
            pygame.display.flip()


def game_quit():
    pygame.quit()
    sys.exit()


game = Game()
