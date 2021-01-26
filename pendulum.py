import pygame
import numpy as np
from pygame.locals import *
import random
import os
import sys

"""m = 1
r=1
m/s
theta from botom ccw
could say both are same just no t2 in 2 and no movement in one"""

def meters_to_pixels(met):
    def met_con(x):
        return round(pix_per_met * x)
    if type(met) is tuple:
        pix = tuple(map(met_con, met))
    else:
        pix = met_con(met)
    return pix


def update_window():
    global pix_per_met, screen_size
    win = pygame.display.set_mode(screen_size, pygame.RESIZABLE)

    # todo add to loop
    screen_size = win.get_size()  # redefine screen_size in loop
    pix_per_met = screen_size[0] / screen_size_meters[0]
    return win


pygame.init()
pygame.mixer.init()
pygame.display.set_caption('Dino')

score_dir = {}
path = os.path.join(os.getcwd(), 'img')  # path.dirname(__file__)
screen_size_meters = (30, 15)

time_mod = 5  # for time
time_multiple = 0
fps = 30  # def mov as pixx/s, m/s and pix/f
dt = 1 / fps
speed = 10

f_rate = 30
pix_per_met = 20
screen_size = tuple(map(meters_to_pixels, screen_size_meters))  # (60, 30)  #
game_window = update_window()

# rects
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
red = pygame.color.Color.r  # correct?

sprites = pygame.sprite.Group()  # list all sps
enemy_sp = pygame.sprite.Group()
lives_sp = pygame.sprite.Group()

vel_fr = meters_to_pixels(speed) / 30  # m/s
g = 9.81


class Mass:
    def __init__(self, m):
        # self.mass = m
        self.size = 2  # rad
        pass


class Rod:
    def __init__(self, r):
        self.rad = r
        pass


class Pendulum:
    def __init__(self, mass, rad):
        self.mass = mass
        self.rad = rad
        self.inert = self.mass * np.abs(self.rad)

        # objects
        self.ball = Mass
        self.rod = 1
        self.pos = (1, 2)

        # self.pos_top = (5,0)
        # positions
        self.theta0 = 0
        self.theta = np.arctan(self.pos[1] / self.pos[0])

        self.ohm = (0, 0, 2)  # k
        self.alph = (0, 0, 0)

        self.vel = (0, 0, 0)
        self.acc = (0, 0, 0)
        self.tension = (0, 0, 0)

        # from other objects
        self.v_pin = (1, 1)
        self.a_pin = (1, 1)
        self.forces = [g]

    def update(self, v_p=(0, 0, 0), a_p=(0, 0, 0)):
        # updates
        self.forces = []
        self.v_pin = v_p  # v other
        self.a_pin = a_p
        self.theta = np.arctan(self.pos[1] / self.pos[0])
        # vel up
        self.ohm = (self.theta - self.theta0) / dt
        self.alph = sum([np.cross(f, self.rad) for f in self.forces]) / self.inert  # convert to vec-sum/dev
        self.theta0 = self.theta  # for dt

        # rest
        rel_vel = np.cross(self.ohm, self.rad)
        self.vel = rel_vel + self.v_pin  # vec
        an = np.cross(self.ohm, rel_vel)
        self.acc = an + np.cross(self.alph, self.rad) + self.a_pin
        self.tension = an - self.forces
        self.pos += self.vel * dt


# Clock object
clock = pygame.time.Clock()
time = 0
state = 'alive'
run = True

# pend object
pend1 = Pendulum(1, 1)
pend2 = Pendulum(1, 1)

# init vals
pend1.forces = [g, pend2.tension]

while run:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False  # breaks loop

        # elif event.type == VIDEORESIZE:
        #     width = event.size
        #     width[1] = int(width[0] / 2)
        #     screen_size = width

        m_pos = pygame.mouse.get_pos()
        m_ck = pygame.mouse.get_pressed(0)
        if m_ck:  # on pos
            # move pend with mouse ceap grave and pin, but loes else from mouse
            pass
        else:
            pend1.forces = [g, pend2.tension]
            pend1.update()
            pend2.update(pend1.vel, pend1.acc)
        # size_fact = max(size)
        # size_ind = size.index(size_fact)  # so we can
        game_window = update_window()
    # pause
    # game_window.fill(BLACK)

    # lives_sp.draw(game_window)
    sprites.draw(game_window)
    # play background
    pygame.display.flip()
pygame.quit()
sys.exit()