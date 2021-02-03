import os
import pygame


def get_high():
    for sc in os.listdir('HighScores'):
        na = sc.replace('_score.txt', '')
        with open(sc) as fi:
            score_dir[na] = fi.read()


def update_window(sc_size, ref_size, pix_ratio):
    win = pygame.display.set_mode(sc_size, pygame.RESIZABLE)

    # todo add to loop
    screen_size = win.get_size()  # redefine screen_size in loop
    pix_ratio = screen_size[0] / ref_size
    return win, pix_ratio


def set_image(img, img_size):
    img_sp = pygame.image.load(img).convert()
    return pygame.transform.scale(img_sp, img_size)


score_dir = {}
