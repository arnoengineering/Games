import pygame
import random
import os


def meters_to_pixels(m):
    return round(pix_per_met * m)


def image_path(img):
    img_path = r'N:\PC stuff\Programs\images'
    return os.path.join(img_path, img)


# todo add max size so not all large
screen_size_meters = (30, 15)
# todo win size in 2:1
time_mod = 5  # for time
fps = 30  # def mov as pixx/s, m/s and pix/f
speed = 10

f_rate = 30
pix_per_met = 20
screen_size = tuple(map(meters_to_pixels, screen_size_meters))  # (60, 30)  #
enemies = ['cactus', 'bird']  # 1,3: low, high def in object or at rand... change prob?
# 3 cac just add 3 sprights

d_path = image_path(r'platformerGraphicsDeluxe_Updated\Player')
# din not image, path
d_p_2 = os.path.join(d_path, 'p1_walk', 'PNG')
dino_imgs = [os.path.join(d_p_2, x) for x in os.listdir(d_p_2) if x.endswith('.png')]
cac_img = os.path.join(d_path, 'p2_stand.png')
bird_img = image_path(r'SpaceShooterRedux\PNG\Enemies\enemyRed3.png')
back_img = image_path(r'planet_3_0.png')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
red = pygame.color.Color.r  # correct?

pygame.init()
pygame.mixer.init()
sprites = pygame.sprite.Group()  # list all sps
enemy_sp = pygame.sprite.Group()

win = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
# todo add to loop
scree_size = win.get_size()  # redefine screen_size in loop
# pix_per_met = scree_size / screen_size_meters

vel_fr = meters_to_pixels(speed) / 30  # m/s


def g_over():
    """get score end loop, get time return ask is replay"""
    pass


def create_enemy():
    enemy = random.choice(enemies)
    starting_pos = screen_size[0] + meters_to_pixels(random.randint(15, 25))
    # time or pos... placehold pos, maybe dif bird,
    # number of ca
    if enemy == 'cactus':
        Cactus(starting_pos)
    else:
        Bird(starting_pos)


def invert_colour():
    screen_cl = [(1, 2, 3)]  # placeholder
    for cl in screen_cl:
        new_cl = map(lambda x: 255 - x, cl)
        print(new_cl)  # place
    pass


def move(time):
    global speed
    if time % time_mod:
        speed += 1

#
# def time_to_frame(ti):
#     return f_rate * ti


class Enemy(pygame.sprite.Sprite):
    def __init__(self, img):  # size for now
        super(Enemy, self).__init__()
        # self.image = pygame.Surface(img)  # fix

        # self.image.fill(BLUE)
        self.image = pygame.image.load(img).convert()
        self.rect = self.image.get_rect()
        enemy_sp.add(self)
        sprites.add(self)  # super/

    def on_screen(self):
        # define x,y max min then test if both x and y are between
        # pos += size for test too, only check y fpr dino and x for other, look both for collision
        if self.rect.right < 0:
            sprites.remove(self)
            create_enemy()

    def update(self):  # same for bird
        self.rect.x -= vel_fr
        self.on_screen()


class Cactus(Enemy):
    def __init__(self, pos):
        super(Cactus, self).__init__(cac_img)
        self.rect.bottom = screen_size[1]
        self.rect.x = pos


class Bird(Enemy):
    def __init__(self, pos_x):
        print(bird_img)
        super(Bird, self).__init__(bird_img)
        # tuple(map(meters_to_pixels, (1, 2)))
        # bird_img
        height_var = meters_to_pixels(random.randint(1, 3))  # hight above ground

        self.rect.x = pos_x
        self.rect.bottom = screen_size[1] - height_var

        pass


class Dino(pygame.sprite.Sprite):
    def __init__(self):
        super(Dino, self).__init__()
        # on init stand
        # on jump jump, on walk loop
        self.img_index = 0
        # init all first to save time?

        self.stand = os.path.join(d_path, 'p1_stand.png')
        self.jump_img = os.path.join(d_path, 'p1_jump.png')
        self.hurt_img = os.path.join(d_path, 'p1_hurt.png')
        self.pos = (4, 5)  # make tupel

        size = (1, 2)
        self.image = pygame.image.load(self.stand).convert()  # fix, hame seperate init so lives are indi
        # from standing and other stuff that resets ev death
        self.lives = 2

        self.rect = self.image.get_rect()
        # self.rect = pygame.Rect(self.pos, size)  # tuple(map()) or. get rect

        # set pos
        self.rect.bottomleft = ((screen_size[0] - size[0]) / 2, screen_size[1])  # botom on ground mid x
        self.air = False
        self.vel = 0

        self.v_jump = -10  # m/2 at jump

        pass

    def death(self):
        ru = True  # ph
        self.lives -= 1
        pygame.image.load(self.hurt_img).convert()
        # do explosion
        if self.lives == 0:
            ru = False
        return ru

    def jump(self):  # maybe add qualifier @... for all
        global run
        # change shape and hight, anima
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:  # check if true always?
            run = False

        if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
            self.image = pygame.image.load(self.jump_img).convert()
            self.air = True
            self.vel = self.v_jump

        if keys[pygame.K_DOWN] or [pygame.K_c]:
            # duck
            pass

    def update(self):

        # def update, then check jump
        # jump only works on ground
        if not self.air:
            # next image of walk
            self.image = pygame.image.load(dino_imgs[self.img_index]).convert()
            self.img_index = (self.img_index + 1) % len(dino_imgs)
            self.jump()

        else:  # either change v0 or take t from start .. put in otherloop, so just loop in air?
            dt = 1 / fps  # cloc.tick...ms since last t - t0  # t0 time at start, then
            self.rect.bottom += meters_to_pixels(self.vel*dt + 4.9 * dt ** 2)
            self.vel += 9.81 * dt
            # print('{}, {}'.format(self.rect.bottom, self.vel))
            if self.rect.bottom >= screen_size[1]:  # y/x?
                self.air = False
                self.rect.bottom = screen_size[1]


def score(time):
    font = pygame.font.Font('freesansbold.ttf', 30)
    # time = 0  # placehold
    score_val = time / 10  # * 100  # 100 points/s
    # location
    text_x = 100  # screen_size - pix_per_caract(fsize)*len
    text_y = 10
    score_out = font.render("Score: " + str(score_val), True, WHITE)
    text_rec = score_out.get_rect()
    text_rec.midtop = (text_x, text_y)
    win.blit(score_out, text_rec)


dino = Dino()
sprites.add(dino)

pygame.display.set_caption('Dino')

# Clock object
clock = pygame.time.Clock()
sc_tim = 0
run = True
# first enemy... set so wait for click
create_enemy()
while run:
    clock.tick(fps)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            ru = False  # breaks loop

    # removes old positions
    sprites.update()
    hits = pygame.sprite.spritecollide(dino, enemy_sp, False)  # add seperate dino list, and chane coll fun

    if hits:
        print(hits)
    #     run = False
    win.fill((0, 0, 0))
    sprites.draw(win)

    sc_tim += clock.get_time()
    score(sc_tim)  # calls score function
    pygame.display.flip()


g_over()  # pause before quit
pygame.quit()
