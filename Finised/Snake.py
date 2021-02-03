import random
import pygame

import tkinter as tk
from tkinter import messagebox

pygame.init()


class Cube(object):
    global rows, width

    def __init__(self, start, dir_nx=1, dir_ny=0, color=(0, 0, 255)):
        self.dir_ny = dir_ny
        self.dir_nx = dir_nx
        self.pos = start
        self.rows = rows
        self.width = width

        # initial momentum
        self.dir_nx = 1
        self.dir_ny = 0

        # change color for snack
        self.color = color

    def move(self, dir_nx, dir_ny):
        self.dir_nx = dir_nx
        self.dir_ny = dir_ny
        # updates x, y values for position
        self.pos = (self.pos[0] + self.dir_nx, self.pos[1] + self.dir_ny)

    def draw(self, surface, eyes=False):
        # draws cube at current location.
        # not necessary, but if i decide to change if this or rows are constant
        dis = self.width // self.rows  # width of each grid cube

        # x, y coordinates of block
        i = self.pos[0]  # Current row
        j = self.pos[1]  # Current Column

        # distance is amount of pixes each column is: prints rectangle at that pixel number. size -2 p for line width
        # form (x pos, y pos, width, height)
        # just change head color maybe
        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))

        # draws eyes
        if eyes:
            # location for eyes
            centre = dis // 2
            radius = 3
            circle_mid = (i * dis + centre - radius, j * dis + 8)
            circle_mid2 = (i * dis + dis - radius * 2, j * dis + 8)
            # separate location for each eye
            pygame.draw.circle(surface, (0, 0, 0), circle_mid, radius)
            pygame.draw.circle(surface, (0, 0, 0), circle_mid2, radius)


class Snake(object):
    # List to hold block objects for snake body
    # snake body length
    body = []

    # dictionary of turn position and direction
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)  # cube at head pos
        self.body.append(self.head)  # adds to list

        # movement direction
        self.dir_nx = 0
        self.dir_ny = 1

    def move(self):
        global run
        # moving the snake
        for event in pygame.event.get():

            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                run = False  # breaks loop

            # check key press
            # elif to make only move in one direction at time
            if keys[pygame.K_LEFT] and self.dir_nx != 1:
                # x set to -1 left Rest follow suit
                self.dir_nx = -1
                self.dir_ny = 0

            elif keys[pygame.K_RIGHT] and self.dir_nx != -1:
                self.dir_nx = 1
                self.dir_ny = 0

            elif keys[pygame.K_UP] and self.dir_ny != 1:
                self.dir_ny = -1
                self.dir_nx = 0

            # so the whole block is visible
            elif keys[pygame.K_DOWN] and self.dir_ny != -1:
                self.dir_ny = 1
                self.dir_nx = 0

            # Turn
            self.turns[self.head.pos[:]] = [self.dir_nx, self.dir_ny]

        # Position list for movement
        for i, c in enumerate(self.body):
            p = c.pos[:]

            # turn block if block is at pos
            if p in self.turns:
                # index of turn
                turn = self.turns[p]
                # x, y coordinates
                c.move(turn[0], turn[1])

                # removes oldest turn if last cube turned
                if i == len(self.body) - 1:
                    self.turns.pop(p)

            # move normally, but don't reach the edge; then loop to other side
            else:
                if c.dir_nx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dir_nx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dir_ny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dir_ny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)

                # Move normally
                else:
                    c.move(c.dir_nx, c.dir_ny)

    def draw(self, surface):
        for i, c in enumerate(self.body):
            # draws eys on first cube
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)

    def add_cube(self):
        # adds cube to last cube in snake
        tail = s.body[-1]
        dx, dy = tail.dir_nx, tail.dir_ny

        # checks tail movement direction; adds cube behind it.
        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        # starts cube moving correctly
        self.body[-1].dir_nx = dx
        self.body[-1].dir_ny = dy

    def reset(self, pos):
        # resets snake after death
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dir_nx = 0
        self.dir_ny = 1


def snack(item):
    global rows
    # location of snack
    position = item.body

    # generates random location until not on snake
    while True:
        # random grid location
        x = random.randrange(rows)
        y = random.randrange(rows)

        # check if block is on snake
        # if z (x, y pos of snack) is same as pos, filter list is > 0 therefore, len > 0 and on snake
        if len(list(filter(lambda z: z.pos == (x, y), position))) > 0:
            continue
        else:
            break

    return x, y


def draw_grid(wid, row, surface):
    # how big grid is
    row_size = wid // row

    # incrementing line draw
    lx = 0
    ly = 0
    for i in range(row):
        lx += row_size
        ly += row_size
        # draw line on x, y = 0:width and same for y, x = 0:width. incrementing for number of lines see above
        pygame.draw.line(surface, (255, 255, 255), (lx, 0), (lx, wid))
        pygame.draw.line(surface, (255, 255, 255), (0, ly), (wid, ly))


def redraw(surface):
    # sets old bos to black
    global rows, width, s, snack_ob

    # removes old positions
    surface.fill((0, 0, 0))

    # draws snake, snack
    s.draw(surface)
    snack_ob.draw(surface)

    score(surface, len(s.body) - 1)  # calls sc function

    draw_grid(width, rows, surface)  # calls function to draw grid
    pygame.display.update()


def score(surface, score_val):
    font = pygame.font.Font('freesansbold.ttf', 30)
    # location
    text_x = 100
    text_y = 10
    score_out = font.render("Score: " + str(score_val), True, (255, 255, 255))
    text_rec = score_out.get_rect()
    text_rec.midtop = (text_x, text_y)
    surface.blit(score_out, text_rec)


# displays message
def message(sub, con):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(sub, con)
    try:
        root.destroy()
    except:
        pass


def main():
    # main function to rule them all
    # Local Variables
    global width, rows, s, run, snack_ob, start_pos

    # Set window size
    win = pygame.display.set_mode((width, width))
    pygame.display.set_caption('Snake')

    # Clock object
    clock = pygame.time.Clock()

    while run:
        pygame.time.delay(50)  # delay for refresh

        # faster for each cube until ten
        if len(s.body) < 5:
            speed = 9 + len(s.body)
        else:
            speed = 15

        clock.tick(speed)

        # move snake
        s.move()

        # check if snake eats snack
        if s.body[0].pos == snack_ob.pos:
            s.add_cube()
            snack_ob = Cube(snack(s), color=(0, 255, 0))

        # checks if snake runs into its game
        # if longer than 1
        for i in range(len(s.body)):
            if s.body[i].pos in list(map(lambda z: z.pos, s.body[(i + 1):])):
                message('You Lost', 'Score: ' + str(len(s.body) - 1))
                # sets restart pos
                s.surve((start_pos, start_pos))
                break
        # calls redraw function
        redraw(win)


# starts game by calling main()

# Play area
width = 500
# so I can change board size: int so it is iterable
rows = int(width / 25)

run = True  # while game is running

# start position for snake must be divisible into row size
start_pos = 10
# Snack, snack objects
s = Snake((0, 0, 255), (start_pos, start_pos))
snack_ob = Cube(snack(s), color=(0, 255, 0))

# starts game
main()
pygame.quit()
