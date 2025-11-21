import pygame
import random
from constants import WIDTH, HEIGHT, CELL, ROWS, GRAY

def draw_grid(win):
    for i in range(0, WIDTH, CELL):
        pygame.draw.line(win, GRAY, (i, 0), (i, HEIGHT))
        pygame.draw.line(win, GRAY, (0, i), (WIDTH, i))


def draw_block(win, color, pos):
    x, y = pos
    pygame.draw.rect(win, color, (x*CELL, y*CELL, CELL, CELL))


def valid(pos, snakes):
    """Check if pos is safe on grid and not in snakes' bodies."""
    x, y = pos
    if x < 0 or x >= ROWS or y < 0 or y >= ROWS:
        return False

    for s in snakes:
        if pos in s.body:
            return False
    return True

def spawn_food(snakes):
    while True:
        x = random.randint(0, ROWS-1)
        y = random.randint(0, ROWS-1)
        if valid((x,y), snakes):
            return (x,y)
