import random
import math
from constants import DIRS
from game_utils import valid

class Snake:
    def __init__(self, color, start, is_smart=True):
        self.color = color
        self.body = [start]
        self.dir = random.choice(DIRS)
        self.alive = True
        self.score = 0
        self.smart = is_smart

    def head(self):
        return self.body[0]

    def move(self, snakes, food):
        if not self.alive:
            return

        if self.smart:
            self.dir = self.smart_move(snakes, food)
        else:
            self.dir = self.q_learning_move(snakes, food)

        new_head = (self.head()[0] + self.dir[0], self.head()[1] + self.dir[1])

        # collision?
        if not valid(new_head, snakes):
            self.alive = False
            return

        # move
        self.body.insert(0, new_head)

        if new_head == food:
            self.score += 1
        else:
            self.body.pop()

    # ---------------------------------------------------------
    # RULE-BASED SMART AI (Snake A)
    # ---------------------------------------------------------
    def smart_move(self, snakes, food):
        best_dir = None
        best_score = -9999

        for d in DIRS:
            nx = self.head()[0] + d[0]
            ny = self.head()[1] + d[1]
            np = (nx, ny)

            if not valid(np, snakes):
                continue

            # heuristic: prefer moves closer to food
            dist_food = -math.dist(np, food)

            # heuristic: more open spaces ahead
            open_cells = 0
            for d2 in DIRS:
                sx = nx + d2[0]
                sy = ny + d2[1]
                if valid((sx,sy), snakes):
                    open_cells += 1
            
            # FIX: Reduced weight for open_cells from 1.5 to 0.5
            # This prevents the snake from being too afraid of walls/corners
            score = dist_food + open_cells * 0.5

            if score > best_score:
                best_score = score
                best_dir = d

        return best_dir if best_dir else self.dir

    # ---------------------------------------------------------
    # Q-LEARNING STYLE AI (Snake B)
    # ---------------------------------------------------------
    def q_learning_move(self, snakes, food):
        best_dir = None
        best_val = -9999

        for d in DIRS:
            nx = self.head()[0] + d[0]
            ny = self.head()[1] + d[1]
            np = (nx, ny)

            if not valid(np, snakes):
                continue

            # reward: closer to food
            reward_food = -math.dist(np, food)

            # penalty: being close to enemy
            enemy = snakes[0].head() if snakes[0] != self else snakes[1].head()
            penalty_enemy = math.dist(np, enemy)

            # penalty: low space available
            free = 0
            for d2 in DIRS:
                sx = nx + d2[0]
                sy = ny + d2[1]
                if valid((sx,sy), snakes):
                    free += 1

            value = reward_food + penalty_enemy*0.4 + free*0.7

            if value > best_val:
                best_val = value
                best_dir = d

        return best_dir if best_dir else self.dir
