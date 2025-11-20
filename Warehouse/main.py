import heapq
import collections
from WarehouseSim import WarehouseSim
from Agent import Agent
from config import *


class BFSAgent(Agent):
    def get_next_move(self, grid, goal, other_agents):
        """Standard BFS to find the next immediate step."""
        queue = collections.deque([(self.pos, [])])
        visited = {self.pos}
        # Treat the other agents as dynamic walls unless they are finished (parked)
        obstacles = {other.pos for other in other_agents if not other.finished}

        while queue:
            current, path = queue.popleft()
            if current == goal:
                return path[0] if path else self.pos

            for neighbor in self.get_neighbors(current, grid, obstacles):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return self.pos # Stay if no path found

class AStarAgent(Agent):
    def heuristic(self, a, b):
        # Manhattan distance
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_next_move(self, grid, goal, other_agents):
        """A* Search to find the next immediate step."""
        # Priority Queue: (f_score, g_score, current_node, path)
        open_set = []
        heapq.heappush(open_set, (0, 0, self.pos, []))
        g_score = {self.pos: 0}
        
        obstacles = {other.pos for other in other_agents if not other.finished}

        while open_set:
            _, current_g, current, path = heapq.heappop(open_set)
            
            if current == goal:
                return path[0] if path else self.pos

            for neighbor in self.get_neighbors(current, grid, obstacles):
                new_g = current_g + 1
                if neighbor not in g_score or new_g < g_score[neighbor]:
                    g_score[neighbor] = new_g
                    f_score = new_g + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, new_g, neighbor, path + [neighbor]))
        
        return self.pos



if __name__ == "__main__":
    # Initialize Agents
    bot_bfs = BFSAgent("BFS Bot", COLOR_BFS, (0, 0))
    
    # Spawn A* slightly offset to avoid start collision
    start_astar = (1, 0) if GRID_HEIGHT > 1 else (0, 1)
    bot_astar = AStarAgent("A* Bot", COLOR_ASTAR, start_astar)
    
    agents = [bot_bfs, bot_astar]
    
    sim = WarehouseSim(agents)
    sim.run()