import pygame
from pygame.locals import *
import random
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
game_window = update_window()

# rects
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
red = pygame.color.Color.r  # correct?

sprites = pygame.sprite.Group()  # list all sps
enemy_sp = pygame.sprite.Group()
# lives_sp = pygame.sprite.Group()

vel_fr = meters_to_pixels(speed) / 30  # m/s


def create_enemy():
    enemy = random.choice(enemies)
    starting_pos = screen_size[0] + meters_to_pixels(random.randint(15, 25))
    # time or pos... placehold pos, maybe dif bird,
    # number of ca
    if enemy == 'bird':
        Bird(starting_pos)
    else:
        c = Cactus(starting_pos)
        if enemy == 'tri':
            Cactus(starting_pos + c.size[0])
            Cactus(starting_pos + 2 * c.size[0])


class Enemy(pygame.sprite.Sprite):
    def __init__(self, img, size):  # size for now
        super(Enemy, self).__init__()
        # self.image = pygame.Surface(img)  # fix

        # self.image.fill(BLUE)
        self.image = set_image(img, size)
        self.rect = self.image.get_rect()
        enemy_sp.add(self)
        sprites.add(self)  # super/

    def update(self):
        # define x,y max min then test if both x and y are between
        # pos += size for test too, only check y fpr dino and x for other, look both for
        self.rect.x -= vel_fr
        if self.rect.right < 0:
            sprites.remove(self)
            create_enemy()


class Cactus(Enemy):
    def __init__(self, pos):
        self.size = meters_to_pixels((1, 2))
        super(Cactus, self).__init__(cac_img, self.size)
        self.rect.bottom = screen_size[1]
        self.rect.x = pos


class Bird(Enemy):
    def __init__(self, pos_x):
        self.size = meters_to_pixels((1, 0.5))
        super(Bird, self).__init__(bird_img, self.size)
        pygame.transform.rotate(self.image, 90)
        # tuple(map(meters_to_pixels, (1, 2)))
        # bird_img
        height_var = meters_to_pixels(random.randint(1, 3))  # hight above ground

        self.rect.x = pos_x
        self.rect.bottom = screen_size[1] - height_var


class Dino(pygame.sprite.Sprite):
    def __init__(self):
        super(Dino, self).__init__()

        self.img_index = 0
        self.lives = 2
        self.size = meters_to_pixels((1, 2))

        # image
        # on init stand; on jump jump, on walk loop
        img_ls = ['stand', 'jump', 'hurt', 'duck']

        self.image_dir = {x: set_image(os.path.join(path, f'p1_{x}.png'), self.size) for x in img_ls}
        self.walk_images = [set_image(os.path.join(d_path, x), self.size)
                            for x in os.listdir(d_path) if x.endswith('.png')]

        self.image = self.image_dir['stand']
        self.rect = self.image.get_rect()

        # set pos
        self.pos = (int(screen_size[0] / 2), screen_size[1])
        self.rect.midbottom = self.pos  # bottom on ground mid x
        self.air = False
        self.duck = False
        self.vel = 0

        self.v_jump = -10  # m/2 at jump
        sprites.add(self)

    def update_size(self):
        self.size = meters_to_pixels((1, 2))
        for x, y in self.image_dir.items():
            self.image_dir[x] = pygame.transform.scale(y, tuple(self.size))

        self.image = self.image_dir['stand']  # fix, same separate init so lives are indie
        self.walk_images = [pygame.transform.scale(x, tuple(self.size)) for x in self.walk_images]
        # from standing and other stuff that resets ev death

        self.rect = self.image.get_rect()
        # set pos
        self.rect.midbottom = self.pos  # bottom on ground mid x

    def live_sp(self):
        live_size = meters_to_pixels((0.5, 0.5))
        live_img = set_image(os.path.join(path, 'Heart.png'), live_size)

        for li in range(self.lives):
            live_rect = live_img.get_rect()
            live_rect.midbottom = (screen_size[0] - 10 - li * live_size[0], screen_size[1])
            game_window.blit(live_img, live_rect)

    def jump(self):  # maybe add qualifier @... for all
        keys = pygame.key.get_pressed()
        # if keys[pygame.K_ESCAPE]:  # check if true always?
        #     menu(sc=level_score)

        if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
            # todo play jump sound
            self.image = self.image_dir['jump']
            self.air = True
            self.vel = self.v_jump

        if self.duck and not (keys[pygame.K_DOWN] or keys[pygame.K_c]):
            self.duck = False
            self.image = self.image_dir['stand']
            self.rect = self.image.get_rect()
            self.rect.midbottom = self.pos

        elif not self.duck and (keys[pygame.K_DOWN] or keys[pygame.K_c]):
            self.image = pygame.transform.rotate(self.image_dir['duck'], -90)
            self.rect = self.image.get_rect()
            self.rect.midbottom = self.pos  #
            self.duck = True

    def update(self):
        # def update, then check jump
        # jump only works on ground
        if not self.air:
            # next image of walk
            self.image = self.walk_images[self.img_index]
            self.img_index = (self.img_index + 1) % len(self.walk_images)
            self.jump()

        else:  # either change v0 or take t from start .. put in otherloop, so just loop in air?
            dt = 1 / fps  # cloc.tick...ms since last t - t0  # t0 time at start, then
            self.rect.bottom += meters_to_pixels(self.vel * dt + 4.9 * dt ** 2)
            self.vel += 9.81 * dt
            # print('{}, {}'.format(self.rect.bottom, self.vel))
            if self.rect.bottom >= screen_size[1]:  # y/x?
                self.air = False
                self.rect.bottom = screen_size[1]


class Game:
    def __init__(self):
        global time_multiple, dino
        self.total_score = 0
        self.level_score = 0
        self.level_num = 0

        # Clock object
        self.clock = pygame.time.Clock()
        self.back_sp = pygame.image.load(back_img).convert()
        self.time = 0
        self.state = 'alive'
        self.run = True

        self.restart()
        self.running()

    def level(self):  # level score?, run indie from level
        # removes old positions
        sprites.update()
        hits = pygame.sprite.spritecollide(dino, enemy_sp, True)  # add seperate dino list, and chane coll fun

        if hits:
            dino.lives -= 1
            dino.image = dino.image_dir['hurt']
            # play sound
            if dino.lives == 0:
                # play d sound
                self.run = False
                self.g_over()
            else:
                self.restart()

        pass

    def menu(self, score=0, de=False):
        button_ls = ['quit']
        if score == 0:  # main men
            button_ls.extend('start')
            dino.image = dino.image_dir['stand']
            print('space jump')

        elif de:  # thus dead
            button_ls.append('restart')
            button_ls.append('save score')
            print(self.score)  # add to list
            print('save?')  # menu option
        else:  # pause
            button_ls.append('resume')
            button_ls.append('main Menu')
            print('pause')

        # create button
        len_b = len(button_ls)
        screen_pos = (screen_size[1] - 40) / len_b
        for b in range(len_b):
            but_pos = (10 + screen_pos) * b
            rec = pygame.Surface((50, but_pos))
            rec.fill(BLUE)
            text_surf = pygame.font.Font('freesansbold.ttf', 30).render(button_ls[b], True, WHITE)
            game_window.blit(text_surf, rec)

        # start = True
        # qui = False  # menu
        # if start:
        #     self.restart()
        # elif qui:
        #     self.quit()

    def running(self):
        global game_window, screen_size
        while self.run:
            self.clock.tick(fps)

            for event in pygame.event.get():
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
                    game_window = update_window()
            if self.state == 'alive':
                # todo level end map
                self.level()
            elif self.state == 'menu':
                self.menu()
            # pause
            game_window.fill(BLACK)
            game_window.blit(pygame.transform.scale(self.back_sp, screen_size), (0, 0))

            dino.live_sp()
            sprites.draw(game_window)

            self.time += self.clock.get_time()
            # play background
            self.score()  # calls score function
            pygame.display.flip()

    def restart(self, from_dead=False):
        global dino
        if from_dead:
            # clear sp
            self.total_score = 0
            self.level_score = 0

            # Clock object
            self.clock = pygame.time.Clock()
            self.time = 0
        self.level_score = 0
        dino = Dino()
        create_enemy()
        # countdown
        # player stand
        pass

    def level_end(self):
        self.total_score += self.level_score
        pygame.time.wait(3000)
        pass

    def pause(self):
        # do something
        self.menu(score=self.level_score)
        pass

    def g_over(self):
        """get score end loop, get time return ask is replay"""
        self.menu(score=self.total_score, de=True)
        pass

    def score(self):
        font = pygame.font.Font('freesansbold.ttf', 30)
        # time = 0  # placehold
        score_val = self.level_score / 10  # * 100  # 100 points/s..self.time from lev
        # location
        text_x = 100  # screen_size - pix_per_caract(fsize)*len
        text_y = 10
        score_out = font.render("Score: " + str(score_val), True, WHITE)
        text_rec = score_out.get_rect()
        text_rec.midtop = (text_x, text_y)
        game_window.blit(score_out, text_rec)

    def save_score(self):
        # ask text
        na = input('name: ')
        with open(na + '_score.txt', 'w') as fi:
            fi.write(str(self.total_score))


def game_quit():
    pygame.quit()
    sys.exit()


dino = Dino()
game = Game()
