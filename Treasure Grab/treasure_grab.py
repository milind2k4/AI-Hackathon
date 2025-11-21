import random
from collections import deque
import time
import os

# ------------------------------
# CONFIG
# ------------------------------
GRID_SIZE = 8
NUM_COINS = 10
DELAY = 1   # For animation


# ------------------------------
# BFS FUNCTION TO FIND PATH
# ------------------------------
def bfs(start, target, grid):
    queue = deque([start])
    visited = set([start])
    parent = {start: None}

    while queue:
        x, y = queue.popleft()

        if (x, y) == target:
            # Reconstruct path
            path = []
            while target:
                path.append(target)
                target = parent[target]
            return path[::-1]  # reverse

        # 4-direction movement
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            nx, ny = x + dx, y + dy

            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y)
                    queue.append((nx, ny))

    return None


# ------------------------------
# PRINT GRID FUNCTION
# ------------------------------
def print_grid(agentA, agentB, coins):
    os.system("cls" if os.name == "nt" else "clear")
    grid = [["." for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    for cx, cy in coins:
        grid[cx][cy] = "C"

    ax, ay = agentA
    bx, by = agentB
    grid[ax][ay] = "A"
    grid[bx][by] = "B"

    for row in grid:
        print(" ".join(row))


# ------------------------------
# MAIN GAME
# ------------------------------
def treasure_grab():
    # Place coins
    coins = set()
    while len(coins) < NUM_COINS:
        coins.add((random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)))
    coins = list(coins)

    # Place agents
    agentA = (0, 0)
    agentB = (GRID_SIZE-1, GRID_SIZE-1)

    scoreA = 0
    scoreB = 0

    # GAME LOOP
    while coins:
        print_grid(agentA, agentB, coins)
        print(f"Coins left: {len(coins)} | A Score: {scoreA} | B Score: {scoreB}")
        time.sleep(DELAY)

        # ------------------------------
        # Agent A turn
        # ------------------------------
        if coins:
            nearest_coin = min(coins, key=lambda c: abs(c[0]-agentA[0]) + abs(c[1]-agentA[1]))
            path = bfs(agentA, nearest_coin, coins)
            if path and len(path) > 1:
                agentA = path[1]  # Move one step

            # Check collection
            if agentA in coins:
                coins.remove(agentA)
                scoreA += 1

        # ------------------------------
        # Agent B turn
        # ------------------------------
        if coins:
            nearest_coin = min(coins, key=lambda c: abs(c[0]-agentB[0]) + abs(c[1]-agentB[1]))
            path = bfs(agentB, nearest_coin, coins)
            if path and len(path) > 1:
                agentB = path[1]

            if agentB in coins:
                coins.remove(agentB)
                scoreB += 1

    # ------------------------------
    # FINAL RESULT
    # ------------------------------
    print_grid(agentA, agentB, [])
    print("\nFINAL RESULTS:")
    print("Agent A Score:", scoreA)
    print("Agent B Score:", scoreB)

    if scoreA > scoreB:
        print("Winner = AGENT A 🏆")
    elif scoreB > scoreA:
        print("Winner = AGENT B 🏆")
    else:
        print("It's a DRAW!")



# Run the game
treasure_grab()
