import pygame
import random
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
caracter_sp = pygame.sprite.Group()  # list all sps
enemy_sp = pygame.sprite.Group()
wall_pp = pygame.sprite.Group()

game_window = pygame.display.set_mode(screen_size)

lev_map = ''  # image to parse

class Wall(pygame.sprite.Sprite):
    def __init__(self):
        super(Wall, self).__init__()
        pass

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super(Food, self).__init__()

class Ghost(pygame.sprite.Sprite):
    def __init__(self, img):
        super(Ghost, self).__init__()
        """def __init__(self, mammalName):
                print(mammalName, 'is a warm-blooded animal.')
                super().__init__(mammalName)"""

        # shold send class over
        self.image = pygame.image.load(img).convert()
        self.rect = self.image.get_rect()
        self.pos = (1, 2)  # placehold
        enemy_sp.add(self)  # super/

    def on_screen(self):
        # define x,y max min then test if both x and y are between
        # pos += size for test too, only check y fpr dino and x for other, look both for collision
        if 0 > self.pos[0]:
            # run continue, or a bunch to start
            self.rand_pos()
            # sprites.remove(self)  # correct?, how about gen 5 then just loop pos

    def rand_pos(self):  # distance on ofscrean

        # item = random.choice(enemies)
        # return pos, item

    # def update(self):  # same for bird
    #     self.rect.x -= speed


class Seeds(Food):
    def __init__(self):
        super(Seeds, self).__init__()
        self.pos = (1, 2)
        # size = (1, 2), change so image takes sise defined
        pass


class Fruit(Food):
    def __init__(self):
        super(Fruit, self).__init__()
        pos = (1, 2)
        size = (1, 2)
        self.rect = pygame.Rect(pos, size)
        self.image = pygame.image.load(bird_img)

        pass


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.pos = (4, 5)  # make tupel
        size = (1, 2)

        pass

    def jump(self):  # maybe add qualifier @... for all
        global run
        # change shape and hight, anima
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:  # check if true always?
            run = False

        if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
            pass
        #
        # if keys[pygame.K_DOWN] or [pygame.K_c]:
        #     # duck
        #     pass

    def update(self):
        pass


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
    game_window.blit(score_out, text_rec)


class Level:  # new map, gen
    def __init__(self):
        pass

pygame.display.set_caption('Snake')

# Clock object
clock = pygame.time.Clock()
run = True

while run:
    clock.tick(fps)
    # pygame.time.delay(50)  # delay for refresh
    # maybe add function
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            ru = False  # breaks loop

    # removes old positions
    sprites.update()
    eat = False
    # collision = pygame.sprite.Group()
    hits = pygame.sprite.spritecollide(dino, sprites, eat)  # add seperate dino list, and chane coll fun
    # else:
    #     play.life -= 1
    # if life = 0 g_over
    if hits:
        run = False
    game_window.fill((0, 0, 0))
    sprites.draw(game_window)

    score()  # calls score function
    pygame.display.update()


g_over()  # pause before quit
pygame.quit()
