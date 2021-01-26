import pygame
import random
import os
import sys


def mine_local():
    # screen grid
    ex = False
    if ex:
        mine_cnt = 20
    else:
        mine_cnt = 0.2 * screen_size[0]*screen_size[1]
    for m in range(mine_cnt):
        mi = Mine(random.random(screen_size[0]), random.random(screen_size[1]))
        mine_sp.add(mi)


pygame.init()
pygame.mixer.init()
pygame.display.set_caption('Dino')

mine_sp = pygame.sprite.Group()
# score_dir = {}
# path = os.path.join(os.getcwd(), 'img')  # path.dirname(__file__)
tile_num = 10
tile_size = 30  # todo add window div by x square
screen_size = (tile_num, tile_num)
pix_size = tile_size * screen_size

time_mod = 5  # for time
time_multiple = 0
fps = 30
# 3 cac just add 3 sprights


def level(self):  # level sc?, run indie from level
    # removes old positions
    sprites.update()
    hits = pygame.sprite.spritecollide(dino, enemy_sp, True)  # add seperate dino list, and chane coll fun

    if hits:
        print(hits)
        dino.lives -= 1
        dino.image = dino.hurt_img
        # play sound
        if dino.lives == 0:
            # play d sound
            self.run = False
            self.g_over()
        else:
            self.restart()

    pass


    # start = True
    # qui = False  # menu
    # if start:
    #     self.restart()
    # elif qui:
    #     self.quit()


def running(self):
    global game_window
    while self.run:
        self.clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False  # breaks loop
                self.quit()

            elif event.type == pygame.locals.VIDEORESIZE:
                width, height = event.size
                height = width / 2

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
        game_window.blit(pygame.transform.scale(self.back_sp, screen_size), (0, 0))
        lives_sp.draw(game_window)
        sprites.draw(game_window)

        self.time += self.clock.get_time()
        # play background
        self.score()  # calls sc function
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
    dino = create_dino(screen_size)
    create_enemy()
    # countdown
    # player stand
    pass


def level_end(self):
    self.total_score += self.level_score
    pygame.time.wait(3000)
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
        pass
