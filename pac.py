import pygame
import random
import numpy as np
from Pathfider import path_finder
time_mod = 5  # for time
fps = 30  # def mov as pixx/s, m/s and pix/f
speed = 2  # m/s
f_rate = 30
pix_per_met = 20
screen_size = (60, 30)  #
enemies = ['cac', 'bird']  # 1,3: low, high def in object or at rand... change prob?
# 3 cac just add 3 sprights

dino_img = ''
cac_img = ''
bird_img = ''

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

pygame.init()
pygame.mixer.init()

all_sp = pygame.sprite.Group()  # mayme make copy of each in here
wall_sp = pygame.sprite.Group()

caracter_sp = pygame.sprite.Group()  # list all sps
enemy_sp = pygame.sprite.Group()

food_sp = pygame.sprite.Group()
live_sp = pygame.sprite.Group()

game_window = pygame.display.set_mode(screen_size)

speed_multiple = 10
lev_map = np.array([])  # image to parse
speed_matrix = np.array([])


class Wall(pygame.sprite.Sprite):
    def __init__(self):
        super(Wall, self).__init__()
        pass


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super(Food, self).__init__()
        food_sp.add(self)


class Seeds(Food):
    def __init__(self):
        super(Seeds, self).__init__()
        self.pos = (1, 2)
        self.score = 10
        # size = (1, 2), change so image takes sise defined
        pass


class Fruit(Food):
    def __init__(self):
        super(Fruit, self).__init__()
        pos = (1, 2)
        size = (1, 2)
        self.score = 50
        self.rect = pygame.Rect(pos, size)
        self.image = pygame.image.load(bird_img)

        pass


class Ghost(pygame.sprite.Sprite):
    def __init__(self, img):
        self.score = 250
        self.velocity = 1
        self.pos = (1, 1)  # grid local
        self.cond = 'chase'
        # change so movementr is fluid, but grid not
        super(Ghost, self).__init__()

        # shold send class over
        self.image = pygame.image.load(img).convert()
        self.rect = self.image.get_rect()
        enemy_sp.add(self)  # super/
        self.target = (1,1)  # pacme...add for diff gosts

    def update(self):  # distance on ofscrean
        pac_pos, pac_vel = 0, 0
        node = False  # place
        old_pos = self.pos

        self.pos += self.velocity * speed_multiple
        if self.cond == 'chase':
            self.chase(pac_pos, pac_vel)
        if node:  # turn
            lev_map[old_pos] = '1'  # wall, rem
            path_finder(lev_map, self.pos, self.target)

    def chase(self, pos, vel):
        
        pass

    def scatter(self):
        pass

    def edible(self):
        pass


class Inky(Ghost):
    def __init__(self):
        super(Inky, self).__init__()
        pass


class Binky(Ghost):
    def __init__(self):
        super(Binky, self).__init__()
        pass


class Pinky(Ghost):
    def __init__(self):
        super(Pinky, self).__init__()
        pass


class Clide(Ghost):
    def __init__(self):
        super(Clide, self).__init__()
        pass


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.pos = (4, 5)  # make tupel
        self.lives = 3  # neet to disp, with spright
        self.size = (1, 2)
        self.eat = False
        pass

    def die(self):
        self.lives -= 1
        # play deth music
        # play death animation
        if self.lives == 0:
            # play g_ov ani
            g_over()

    def update(self):
        pass


class Level:  # new map, gen
    def __init__(self):
        # creat map
        # add food
        # tot sc += 1000
        pass

    def reset_lev(self):
        pac_pos = 1  # place
        gost_pos = 0  # center, maybe rem all and reinti


def reset_game():
    pac.die()
    # level rest, mayme in here


def collision():
    global scor
    wall_collision = pygame.sprite.groupcollide(enemy_sp, wall_sp, False, False)  # all groups
    # food, indi sc
    food_col = pygame.sprite.spritecollide(pac, food_sp, True)
    for foo in food_col:  # kill...
        if foo is Fruit:
            pac.eat = True  # set timer
        scor += foo.score
    # en
    hits = pygame.sprite.spritecollide(pac, enemy_sp, False)  # add seperate dino list, and chane coll fun
    if pac.eat:
        for hit in hits:
            scor += hit.score
            hit.pos = (0, 0)  # plachold
    else:
        reset_game()


def score():
    font = pygame.font.Font('freesansbold.ttf', 30)
    time = 0  # placehold
    score_val = time * 100  # 100 points/s
    # location
    text_x = 100
    text_y = 10
    score_out = font.render("Score: " + str(score_val), True, (255, 255, 255))
    text_rec = score_out.get_rect()
    text_rec.midtop = (text_x, text_y)

    # lives
    live_hight = screen_size[1] - 20  # test

    # 20 px from right, 20px fom other
    for x in range(pac.lives):
        li = Player()
        li.pos.right = screen_size[0] - 20 - (li.size[0] + 20) * x  # rect/cir/roght
        li.pos.bottom = live_hight
        # only add if diffent
        live_sp.add(li)
    # add to sprints, dond move, only have pos
    game_window.blit(score_out, text_rec)


def g_over():
    pass


pygame.display.set_caption('PacMan')

pac = Player()  # new lev,  todo add menu, highscore, restart
clock = pygame.time.Clock()
scor = 0
run = True
# first enemy... set so wait for click
# create_enemy()
while run:
    clock.tick(fps)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            ru = False  # breaks loop

    # removes old positions
    all_sp.update()
    # collision = pygame.sprite.Group()

    game_window.fill((0, 0, 0))
    all_sp.draw(game_window)
    score()  # calls sc function
    pygame.display.flip()


g_over()  # pause before quit
pygame.quit()
