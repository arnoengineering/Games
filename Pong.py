import pygame
import random
import tkinter
import sys
from tkinter import messagebox

pygame.init()


# Defines ball object and ai t0o move paddle
class Ball(object):
    def __init__(self, pos):
        global border_h, size
        # lowest pos
        self.low = size - border_h
        self.color = (255, 255, 255)

        # x, y pos and starting velocity of ball
        self.x = pos[0]
        self.y = pos[1]
        self.vx = 0
        self.vy = 0
        # ball size pixels
        self.ball_s = 15

    # changes angle and velocity for ball bouncing
    def bounce(self):
        global pad2pos, vel_y1, vel_y2

        # paddle height might need to change
        pad_h = pad_size * 3

        # if ball hits borders
        if self.y <= 0 or (self.y + self.ball_s) >= self.low:
            self.vy = -self.vy

        # awards points if hits goal line
        elif self.x <= 0:
            sb.score_add('p1')
            surve('p1')

        elif self.x >= (size - self.ball_s):
            sb.score_add('p2')
            surve('p2')

        # checks paddle collision
        # checks x pos then y pos
        if (self.x + self.ball_s) >= pad1pos[0]:  # checks this if over threshold

            # Paddle location: since can hit wide on each, that is why double
            pad_loc = list(range(pad1pos[1], (pad1pos[1] + pad_h + self.ball_s)))

            if (self.y + self.ball_s - 1) in pad_loc:
                # x velocity rebounds: abs so I can set direction
                self.vx = -abs(self.vx)
                self.vy += int(vel_y1 / 2)  # imparts momentum

        # Checks position for paddle 2
        elif (self.x - self.ball_s) <= pad2pos[0]:

            # since can hit wide on each
            pad_loc = list(range(pad2pos[1], (pad2pos[1] + pad_h + self.ball_s)))

            if (self.y + self.ball_s - 1) in pad_loc:
                # x velocity rebounds: abs so I can set direction
                self.vx = abs(self.vx)
                self.vy += int(vel_y1 / 2)  # imparts momentum

        # adjust position based on velocity
        self.x += self.vx
        self.y += self.vy

    # defines ball behavior after a sc, before release
    def startup(self, pos_x, pos_y, rel, release=False):
        # position of ball on startup: called with paddle positions. Sticks to paddle
        self.x = pos_x
        self.y = pos_y

        # velocity once released
        if release:
            self.vx = rel[0]
            self.vy = rel[1]

    # function to move paddle on one player mode
    def ai_pad(self):

        global vy_max, pad2pos

        # only runs when ball is moving to the left
        if self.vx < 0:
            ang = self.vy // self.vx  # essentially arc_tan, but I'm just taking tran again so no need to import.

            # Sign convention is weird so I don't have to use absolute value, com just works correctly
            y_int = self.y - int(self.x * ang)

            # removes div by zero error, uses trig to find x location at bounce then uses this to solve y location
            if y_int < 0 and ang != 0:
                x_col = self.x - (self.y / ang)  # x bounce location
                y_int = int(x_col * ang)

            # same as above only for top bounce
            elif y_int > size and ang != 0:
                x_col = self.x + (size - self.y) / ang
                y_int = size + int(x_col * ang)  # since neg

            # moves paddle one step per cycle to keep it the same speed
            if pad2pos[1] < y_int:
                pad2.move(vy_max, pad2pos)
            if pad2pos[1] > y_int:
                pad2.move(-vy_max, pad2pos)
            else:
                pad2.move(0, pad2pos)

    # tells how to draw the ball object
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.ball_s, self.ball_s))


# class to move paddles every cycle: class since I want to re initialise their positions
class MovePad(object):
    def __init__(self, ai_run=False):
        self.ai = ai_run
        # random velocity to be used at startup of one player mode
        self.rand_v = random.randrange(-10, 10)

    # sets y velocity then calls paddle objects to move them that may pixels every cycle
    def move_pad(self, hold_y1, hold_y2, st_play, ran, cnt):
        global run, pad1, vy_max

        # Holds current x, y velocity so don't hve to adjust
        vy, vy2 = hold_y1, hold_y2

        # value to tell if the ball has been released then the startup can be ended
        rel = False

        pygame.key.set_repeat()
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False  # breaks loop
                break

            # hold down keys
            # opposite from who gets ball
            if event.type == pygame.KEYDOWN:
                if st_play == 'p2' and event.key == pygame.K_LEFT:
                    rel = True
                elif st_play == 'p1' and event.key == pygame.K_d and not self.ai:
                    rel = True
                if event.key == pygame.K_UP:
                    vy = -vy_max
                elif event.key == pygame.K_DOWN:
                    vy = vy_max

                if not self.ai:
                    if event.key == pygame.K_w:
                        vy2 = -vy_max
                    elif event.key == pygame.K_s:
                        vy2 = vy_max

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    vy = 0
                if not self.ai and (event.key == pygame.K_w or event.key == pygame.K_s):
                    vy2 = 0

        # calls paddle objects
        pad1.move(vy, pad1pos)
        if self.ai:
            # will make random movements then release ball
            if st_play == 'p1':
                if not rel:
                    cnt += 1

                    # random vel
                    # only changes vel every 10 cycles
                    if cnt % 10 == 0:
                        self.rand_v = random.randrange(-10, 10)
                    pad2.move(self.rand_v, pad2pos)

                    if cnt > ran:
                        # releases
                        rel = True
            # otherwise move according to trig
            else:
                b.ai_pad()
        else:
            pad2.move(vy2, pad2pos)

        return vy, vy2, rel, cnt


class Paddle(object):
    def __init__(self, pos, color, s, siz):
        self.size = siz
        self.x = pos[0]
        self.y = pos[1]
        self.vy = 0
        self.vx = 0
        self.color = color
        self.b_size = s
        self.pad_size = self.b_size * 3

    def reset_pos(self, pos):
        # resets paddle pos

        self.y = int(self.size / 2)
        pos[1] = self.y

    def move(self, v, pos):
        # only moves in bounds

        # pass for syntax
        if self.y <= 0 and v < 0:
            pass
        elif (self.y + self.pad_size) >= self.size and v > 0:
            pass
        # only adds vel if not off board
        else:
            self.y += v
            # to reference out
            pos[1] += v

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.b_size, self.pad_size))


# object so sc holds value
class ScoreBoard(object):
    def __init__(self):
        # initial scores
        self.p1_score = 0
        self.p2_score = 0

        self.win_score = 7

    def score_add(self, pad):

        # adds sc
        if pad == 'p1':
            self.p1_score += 1

        elif pad == 'p2':
            self.p2_score += 1

        if self.p1_score == self.win_score or self.p2_score == self.win_score:
            message(pad)

    def score_output(self, surface):
        # outputs sc
        global size

        font = pygame.font.SysFont('arial', 24)
        # location text 1 3/4, text2 1/4 on top1
        text1 = (int(3 * size / 4), 10)
        text2 = (int(size / 4), 10)

        # renders scores
        score1 = font.render(("Score: " + str(self.p1_score)), True, (255, 255, 255))
        score2 = font.render(("Score: " + str(self.p2_score)), True, (255, 255, 255))
        # creates objects
        text1_rec = score1.get_rect()
        text2_rec = score2.get_rect()

        text1_rec.midtop = text1
        text2_rec.midtop = text2

        # outputs
        surface.blit(score1, text1_rec)
        surface.blit(score2, text2_rec)


class StartMessage(object):
    def __init__(self):
        self.top = tkinter.Tk()

    # creates buttons on startup
    def game_mode(self):

        text = tkinter.Label(self.top, text="How many players?")

        b1 = tkinter.Button(self.top, text="1 Player", command=lambda: self.rem(ai_r=True))
        b2 = tkinter.Button(self.top, text="2 Player", command=lambda: self.rem(ai_r=False))

        # puts onto window
        text.pack()
        b1.pack()
        b2.pack()
        self.top.mainloop()

    def rem(self, ai_r=False):
        self.top.destroy()
        # initializes the move object with correct players
        mb.__init__(ai_run=ai_r)


def message(winner):
    global run
    # stops loop
    run = False
    # prints message if someone wins
    if winner == 'p1':
        winner = "Player 1"
    else:
        winner = "Player 2"
    # sees if they want to continue
    cont = messagebox.askyesno((winner + " Wins!"), "Would you like to play again")

    if cont:
        main()

    else:
        pygame.quit()
        sys.exit("GG: Have a nice day")


def redraw(surface):
    global b, pad1, pad2, border_h, size

    # fill old surfaces
    surface.fill((0, 0, 0))

    # draw objects
    b.draw(surface)
    pad1.draw(surface)
    pad2.draw(surface)

    # bottom border, center_line
    pygame.draw.rect(win, (255, 255, 255), (0, (size - border_h), size, border_h))
    pygame.draw.line(surface, (255, 255, 255), ((size // 2), 0), ((size // 2), size))

    # calls sc without player
    sb.score_output(win)
    pygame.display.update()


# if someone scores then this will run until start then main
def surve(player):
    global clock, pad1pos, pad2pos, win, run, pad1, pad2, vy_max
    #
    # change v_hold
    vy1, vy2 = 0, 0

    # rests position to center
    redraw(win)

    pad1.reset_pos(pad1pos)
    pad2.reset_pos(pad2pos)
    # random variables for release
    rand_t = random.randrange(5, 50)
    rand_count = 0

    start = True
    # calls movement
    while start:
        # skips if quit
        if not run:
            break
        # timing elements: since this is the start loop and main doesnt run.
        pygame.time.delay(50)
        clock.tick(10)

        # calls move paddle check if released
        vy1, vy2, rel_val, rand_count = mb.move_pad(vy1, vy2, player, rand_t, rand_count)
        redraw(win)
        # sets ball to correct player
        if player == 'p1':
            # 5 pixels to right
            bx_pos = pad2pos[0] + 30
            by_pos = pad2pos[1]
            rel_v = [vy_max, vy2]

        else:
            bx_pos = pad1pos[0] - 30  # adjust if ball size
            by_pos = pad1pos[1]
            rel_v = [-vy_max, vy1]

        # returns to main loop after release
        if rel_val:
            start = False

        b.startup(bx_pos, by_pos, rel_v, rel_val)


def main():
    global b, run, size, clock, win, vel_y1, sb, vel_y2, pad1, pad2, vel_y1, vel_y2, vy_max

    # initializes objects
    b = Ball(pad1pos)
    sb = ScoreBoard()

    # increases velocity as game goes on
    speed_in = 0

    # calls sc
    sb.score_output(win)

    # coin toss
    coin = random.randint(0, 1)
    if coin == 0:
        p = 'p1'
        pl = 2
    else:
        p = 'p2'
        pl = 1

    print("coin toss won py player: ", pl)
    print("controls: P1:'arrow keys', P2:'wasd'")
    pygame.time.delay(2000)

    surve(p)

    # resets run to true
    run = True
    while run:

        speed_in += 1

        # increases speed every 100 cycles to max of 20
        if speed_in % 100 == 0:
            vy_max += 1

        pygame.time.delay(50)
        clock.tick(15)

        # calls function to move paddles
        redraw(win)
        # player = none
        vel_y1, vel_y2, rel, co = mb.move_pad(vel_y1, vel_y2, "", 0, 0)
        b.bounce()


# initializing
# max pad speed
vy_max = 15

# vy changing
vel_y1, vel_y2 = 0, 0

# pixel size
size = 500

# window initializing
win = pygame.display.set_mode((size, size))
pygame.display.set_caption('Pong')

# paddle start location
pad_loc_s = int(size / 2)
pad_size = 20

# position


pad1pos = [size - 35, pad_loc_s]
pad2pos = [10, pad_loc_s]

border_h = 20

# creates objects on startup
b = Ball(pad1pos)
sb = ScoreBoard()

# test game mode
# game_mode(top)
# initializes objects
sm = StartMessage()

mb = MovePad()
# calls startup messages
sm.game_mode()

run = True
# change 25 and 30 for size ad variable
pad1 = Paddle(pad1pos, (255, 255, 255), pad_size, size)
pad2 = Paddle(pad2pos, (255, 255, 255), pad_size, size)

# Clock object
clock = pygame.time.Clock()

main()
