import random

class Agent:
    def __init__(self, name, color, start_pos):
        self.name = name
        self.color = color
        self.pos = start_pos
        self.path_history = [start_pos]
        self.finished = False
        self.steps = 0

    def get_next_move(self, grid, goal, other_agents):
        raise NotImplementedError

    def get_neighbors(self, node, grid, dynamic_obstacles=None):
        height = len(grid)
        width = len(grid[0])
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(directions) # Randomize exploration
        
        neighbors = []
        r, c = node
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                if grid[nr][nc] == 0: # Wall check
                    if dynamic_obstacles and (nr, nc) in dynamic_obstacles:
                        continue # Collision check
                    neighbors.append((nr, nc))
        return neighbors