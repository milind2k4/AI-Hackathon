import pygame
import random
from collections import deque
import heapq
import time
pygame.init()
ROWS = 20
COLS = 30
CELL_SIZE = 30
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Agents With BFS and A*")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255,255,0)
grid = [["-" for _ in range(COLS)] for _ in range(ROWS)]
spawn_timer = 0
SPAWN_INTERVAL = 100
MAX_RESOURCES = 10
resources = deque()
clock = pygame.time.Clock()
agent1 = [0, 0]   # BFS (Blue)
agent2 = [9, 9]   # A* (Red)
agent3 = [0, 9]   # DFS (Yellow)
path1 = []
path2 = []
path3 = []
blue_score = 0
red_score = 0
yellow_score = 0
GAME_DURATION = 10 # seconds
start_time = time.time()
# =========================================================================
# BFS
# =========================================================================
def bfs(start, goal):
    queue = deque([tuple(start)])
    visited = set([tuple(start)])
    parent = {}
    while queue:
        r, c = queue.popleft()
        if [r, c] == goal:
            return reconstruct(parent, start, goal)
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and (nr, nc) not in visited:
                visited.add((nr, nc))
                parent[(nr, nc)] = (r, c)
                queue.append((nr, nc))
    return []
# =========================================================================
# A*
# =========================================================================
def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])
def astar(start, goal):
    pq = []
    heapq.heappush(pq, (0, tuple(start)))
    g = {tuple(start): 0}
    parent = {}
    while pq:
        _, current = heapq.heappop(pq)
        r, c = current
        if [r, c] == goal:
            return reconstruct(parent, start, goal)
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                new_cost = g[(r,c)] + 1

                if (nr, nc) not in g or new_cost < g[(nr, nc)]:
                    g[(nr, nc)] = new_cost
                    priority = new_cost + heuristic((nr, nc), goal)
                    heapq.heappush(pq, (priority, (nr, nc)))
                    parent[(nr, nc)] = (r, c)
    return []
# =========================================================================
# Reconstruct path
# =========================================================================
def dfs(start, goal):
    stack = [tuple(start)]
    visited = set([tuple(start)])
    parent = {}

    while stack:
        r, c = stack.pop()

        if [r, c] == goal:
            return reconstruct(parent, start, goal)

        # DFS: reverse order for deep-first priority
        for dr, dc in [(1,0),(0,1),(0,-1),(-1,0)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and (nr, nc) not in visited:
                visited.add((nr, nc))
                parent[(nr, nc)] = (r, c)
                stack.append((nr, nc))

    return []

def reconstruct(parent, start, goal):
    path = []
    curr = tuple(goal)
    while curr != tuple(start):
        path.append(list(curr))
        curr = parent.get(curr)
        if curr is None:
            return []
    path.reverse()
    return path
# =========================================================================
# Resource spawn
# =========================================================================
def spawn_resource():
    r = random.randint(0, ROWS-1)
    c = random.randint(0, COLS-1)
    if [r, c] == agent1 or [r, c] == agent2:
        return
    grid[r][c] = "R"
    resources.append((r, c))
    # if len(resources) > MAX_RESOURCES:
    #     old_r, old_c = resources.popleft()
    #     grid[old_r][old_c] = "-"
# =========================================================================
# Draw function
# =========================================================================
def draw_grid():
    WIN.fill(WHITE)
    for r in range(ROWS):
        for c in range(COLS):
            rect = pygame.Rect(c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid[r][c] == "R":
                pygame.draw.rect(WIN, GREEN, rect)
            else:
                pygame.draw.rect(WIN, WHITE, rect)
            pygame.draw.rect(WIN, BLACK, rect, 1)
    pygame.draw.rect(WIN, BLUE, (agent1[1]*CELL_SIZE, agent1[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(WIN, RED, (agent2[1]*CELL_SIZE, agent2[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(WIN, YELLOW, (agent3[1]*CELL_SIZE, agent3[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.update()
# =========================================================================
# MAIN LOOP
# =========================================================================
running = True
while running:
    # END GAME AFTER 20 SECONDS
    if time.time() - start_time >= GAME_DURATION:
        print("\n=========== RESULT ===========")
        print("Blue Collected :", blue_score)
        print("Red Collected  :", red_score)
        print("Yellow (DFS) :", yellow_score)
        print("================================\n")
        running = False
        continue
    dt = clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    spawn_timer += dt
    if spawn_timer >= SPAWN_INTERVAL:
        spawn_resource()
        spawn_timer = 0
        # new target = first resource
        if resources:
            goal = list(resources[0])
            path1 = bfs(agent1, goal)
            path2 = astar(agent2, goal)
            path3 = dfs(agent3, goal)
    if path2:
        agent2[:] = path2.pop(0)
    if path1:
        agent1[:] = path1.pop(0)
    if path3:
        agent3[:] = path3.pop(0)
    # Check pickups
    if resources:
        tr, tc = resources[0]
        if agent1 == [tr, tc]:
            blue_score += 1
            grid[tr][tc] = "-"
            resources.popleft()
            path1 = []
            path2 = []
        elif agent2 == [tr, tc]:
            red_score += 1
            grid[tr][tc] = "-"
            resources.popleft()
            path1 = []
            path2 = []
        elif agent3 == [tr, tc]:
            yellow_score += 1
            grid[tr][tc] = "-"
            resources.popleft()
            path1 = path2 = path3 = []
    draw_grid()
pygame.quit()