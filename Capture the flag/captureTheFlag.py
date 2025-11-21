import heapq
import time
import os

# Terminal colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# ------------------ A* PATHFINDING ------------------
def astar(start, goal, grid):
    rows, cols = len(grid), len(grid[0])
    pq = [(0, start)]
    came_from = {start: None}
    g = {start: 0}

    def h(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    while pq:
        _, current = heapq.heappop(pq)

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx, ny = current[0]+dx, current[1]+dy
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] != '#':
                neighbor = (nx, ny)
                new_cost = g[current] + 1

                if neighbor not in g or new_cost < g[neighbor]:
                    g[neighbor] = new_cost
                    f = new_cost + h(neighbor, goal)
                    heapq.heappush(pq, (f, neighbor))
                    came_from[neighbor] = current

    return None

# ------------------ AGENT ------------------
class Agent:
    def __init__(self, name, pos, flag_pos, enemy_flag_pos, grid):
        self.name = name
        self.pos = pos
        self.home_flag = flag_pos
        self.enemy_flag = enemy_flag_pos
        self.grid = grid
        self.has_flag = False

    def in_defense_zone(self, enemy_pos):
        return abs(enemy_pos[0] - self.home_flag[0]) + abs(enemy_pos[1] - self.home_flag[1]) <= 4

    def choose_action(self, enemy_pos):
        # returning home with flag
        if self.has_flag:
            return astar(self.pos, self.home_flag, self.grid)[1]

        # chasing enemy
        if self.in_defense_zone(enemy_pos):
            return astar(self.pos, enemy_pos, self.grid)[1]

        # attacking
        return astar(self.pos, self.enemy_flag, self.grid)[1]

    def move(self, new_pos):
        self.pos = new_pos


# ------------------ PRINT GRID WITH COLORS ------------------
def print_grid(grid, A_pos, B_pos, A_flag, B_flag, agentA, agentB):

    temp = [row[:] for row in grid]

    ax, ay = A_pos
    bx, by = B_pos

    # Draw flags only if NOT captured
    if not agentB.has_flag:
        temp[B_flag[0]][B_flag[1]] = RED + "F" + RESET   # B's red flag
    if not agentA.has_flag:
        temp[A_flag[0]][A_flag[1]] = GREEN + "F" + RESET # A's green flag

    # Draw agents
    if agentA.has_flag:
        temp[ax][ay] = YELLOW + "A*" + RESET
    else:
        temp[ax][ay] = "A"

    if agentB.has_flag:
        temp[bx][by] = YELLOW + "B*" + RESET
    else:
        temp[bx][by] = "B"

    # Print grid
    for row in temp:
        print("".join(row))
    print()


# ------------------ SIMULATION ------------------
def simulate():
    grid_raw = [
        "###################",
        "#F....#.....#.....#",
        "#..##...#...#..#..#",
        "#..#......#....#..#",
        "#..#.........##...#",
        "#.....#......##...#",
        "#..#........#.....#",
        "###################"
    ]

    grid = [list(row) for row in grid_raw]

    A_flag = (1, 1)
    B_flag = (6, 15)

    A_start = A_flag
    B_start = B_flag

    agentA = Agent("A", A_start, A_flag, B_flag, grid)
    agentB = Agent("B", B_start, B_flag, A_flag, grid)

    for t in range(400):
        clear()
        print(f"Turn: {t}")

        print_grid(grid, agentA.pos, agentB.pos, A_flag, B_flag, agentA, agentB)

        # movement decisions
        a_next = agentA.choose_action(agentB.pos)
        b_next = agentB.choose_action(agentA.pos)

        agentA.move(a_next)
        agentB.move(b_next)

        # flag capture
        if agentA.pos == agentA.enemy_flag and not agentA.has_flag:
            agentA.has_flag = True
            print(YELLOW + "A has captured B's flag!" + RESET)

        if agentB.pos == agentB.enemy_flag and not agentB.has_flag:
            agentB.has_flag = True
            print(YELLOW + "B has captured A's flag!" + RESET)

        # win conditions
        if agentA.has_flag and agentA.pos == agentA.home_flag:
            clear()
            print(GREEN + "AGENT A RETURNS WITH THE FLAG — A WINS!" + RESET)
            return

        if agentB.has_flag and agentB.pos == agentB.home_flag:
            clear()
            print(RED + "AGENT B RETURNS WITH THE FLAG — B WINS!" + RESET)
            return

        time.sleep(1.0)

    print("Draw: Time up")


simulate()
