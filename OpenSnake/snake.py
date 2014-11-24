######################################################################
# OpenSnake
#
# Classic snake game with the possibility to give commands through an
# XML file.
#
# Commands:
# Left: change direction (anticlockwise)
# Right: change direction (clockwise)
#
# XML syntax:
# <direction>1</direction> ====> LEFT
# <direction>-1</direction> ====> RIGHT
# <direction></direction> ====> STRAIGHT
#
# Configuration constants:
# - WALL_TELEPORTER: if enabled, the snake doesn't die if it hit the wall
#
# Modes to play:
# 1. using keyboard
# 2. using XML commands
#
# Using:
# python snake.py [mode=1]
#
#
# Developed by: Davide Valeriani
#		School of Computer Science and Electronic Engineering
#               University of Essex
#
######################################################################

import pygame, random, sys
from pygame.locals import *
from xml.dom import minidom


def collide(p1, p2):
    if p1 == p2:
        return True
    return False


def die(screen, score, message):
    f = pygame.font.SysFont('Arial', 30)
    if message == "SNAKE":
        t = f.render('You ate yourself!', True, TEXT_COLOR)
    else:
        t = f.render('You hit the wall!', True, TEXT_COLOR)
    screen.blit(t, (10, 200))
    t = f.render('Your score was: '+str(score)+' points', True, TEXT_COLOR)
    screen.blit(t, (10, 270))
    pygame.display.update()


# Configuration constants
SPEED = 20
WALL_TELEPORTER = 1
SCREEN_SIZE = (800, 600)
CELL_SIZE = 20  # pixels
# Directions
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3
# MODES
KEYBOARD = 1
BCI = 2
# COLORS
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 0, 255)
BACKGROUND_COLOR = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)
# Mode
if len(sys.argv) > 1:
    mode = int(sys.argv[1])
else:
    mode = 1

screen_cells = (SCREEN_SIZE[0] / CELL_SIZE, SCREEN_SIZE[1] / CELL_SIZE)
# Snake coordinates
snake = [(screen_cells[0] / 2, screen_cells[1] / 2 + 1),
         (screen_cells[0] / 2, screen_cells[1] / 2),
         (screen_cells[0] / 2, screen_cells[1] / 2 - 1)]
# Default direction
dirs = DOWN
score = 0
# Position of the apple
apple_pos = (random.randint(1, screen_cells[0]-1), random.randint(1, screen_cells[1]-1))
# Control that the new apple does not appear in the snake's body
while apple_pos in snake:
    apple_pos = (random.randint(1, screen_cells[0]-1), random.randint(1, screen_cells[1]-1))

pygame.init()
s = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Snake')
apple_image = pygame.Surface((CELL_SIZE, CELL_SIZE))
apple_image.fill(APPLE_COLOR)
# Snake image
img = pygame.Surface((CELL_SIZE, CELL_SIZE))
img.fill(SNAKE_COLOR)
f = pygame.font.SysFont('Arial', 20)
clock = pygame.time.Clock()
dead = False
while not dead:
    clock.tick(SPEED)
    s.fill(BACKGROUND_COLOR)
    # Update the direction
    if mode == KEYBOARD:
        # Keyboard
        for e in pygame.event.get():
            if e.type == QUIT:
                sys.exit(0)
            elif e.type == KEYDOWN:
                if e.key == K_LEFT:
                    if dirs == UP:
                        dirs = LEFT
                    elif dirs == LEFT:
                        dirs = DOWN
                    elif dirs == DOWN:
                        dirs = RIGHT
                    elif dirs == RIGHT:
                        dirs = UP
                elif e.key == K_RIGHT:
                    if dirs == UP:
                        dirs = RIGHT
                    elif dirs == RIGHT:
                        dirs = DOWN
                    elif dirs == DOWN:
                        dirs = LEFT
                    elif dirs == LEFT:
                        dirs = UP
    elif mode == BCI:
        for e in pygame.event.get():
            if e.type == QUIT:
                sys.exit(0)
        xml_doc = minidom.parse('commands.xml')
        item_list = xml_doc.getElementsByTagName('direction')
        if len(item_list[0].childNodes) > 0:
            selected_direction = int(item_list[0].childNodes[0].nodeValue.replace('\n', ''))
            if selected_direction == LEFT:
                if dirs == UP:
                    dirs = LEFT
                elif dirs == LEFT:
                    dirs = DOWN
                elif dirs == DOWN:
                    dirs = RIGHT
                elif dirs == RIGHT:
                    dirs = UP
            elif selected_direction == RIGHT:
                if dirs == UP:
                    dirs = RIGHT
                elif dirs == RIGHT:
                    dirs = DOWN
                elif dirs == DOWN:
                    dirs = LEFT
                elif dirs == LEFT:
                    dirs = UP
    # Move the snake
    for i in range(1, len(snake))[::-1]:
        snake[i] = snake[i-1]
    if dirs == DOWN:
        snake[0] = (snake[0][0], snake[0][1] + 1)
    elif dirs == RIGHT:
        snake[0] = (snake[0][0] + 1, snake[0][1])
    elif dirs == UP:
        snake[0] = (snake[0][0], snake[0][1] - 1)
    elif dirs == LEFT:
        snake[0] = (snake[0][0] - 1, snake[0][1])
    # Check collisions with the snake body
    for i in range(1, len(snake)):
        if collide(snake[0], snake[i]):
            die(s, score, "SNAKE")
            dead = True
    if collide(snake[0], apple_pos):
        score += 1
        snake.append((700, 700))
        apple_pos = (random.randint(1, screen_cells[0]-1), random.randint(1, screen_cells[1]-1))
        # Control that the new apple does not appear in the snake's body
        while apple_pos in snake:
            apple_pos = (random.randint(1, screen_cells[0]-1), random.randint(1, screen_cells[1]-1))
    # Check wall collision
    if snake[0][0] < 0 or snake[0][0] >= screen_cells[0] or snake[0][1] < 0 or snake[0][1] >= screen_cells[1]:
        if not WALL_TELEPORTER:
            print "You hit the wall!"
            die(s, score, "WALL")
            dead = True
        else:
            if snake[0][0] < 0:
                snake[0] = (screen_cells[0], snake[0][1])
            elif snake[0][0] >= screen_cells[0]:
                snake[0] = (0, snake[0][1])
            elif snake[0][1] < 0:
                snake[0] = (snake[0][0], screen_cells[1])
            elif snake[0][1] >=  screen_cells[1]:
                snake[0] = (snake[0][0], 0)
    for i in range(len(snake)):
        s.blit(img, (snake[i][0]*CELL_SIZE, snake[i][1]*CELL_SIZE))
    s.blit(apple_image, (apple_pos[0]*CELL_SIZE, apple_pos[1]*CELL_SIZE))
    t = f.render(str(score), True, TEXT_COLOR)
    s.blit(t, (10, 10))
    pygame.display.update()

while True:
    for e in pygame.event.get():
        if e.type == QUIT:
            sys.exit(0)
