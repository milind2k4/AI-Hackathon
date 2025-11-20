import sys
import pygame
import random
from config import *

class WarehouseSim:
    def __init__(self, agents):
        pygame.init()
        self.width_cells = GRID_WIDTH
        self.height_cells = GRID_HEIGHT
        self.screen_w = self.width_cells * CELL_SIZE
        self.screen_h = self.height_cells * CELL_SIZE
        
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))
        pygame.display.set_caption("Warehouse Logic: BFS vs A*")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 16)

        # Environment Setup
        self.grid = self._generate_grid(OBSTACLE_DENSITY)
        # random goal position
        self.goal = (random.randint(0, self.height_cells - 1), random.randint(0, self.width_cells - 1))
        
        self.agents = agents

        # Clear critical zones
        for agent in self.agents:
            r, c = agent.pos
            self.grid[r][c] = 0
        
        gr, gc = self.goal
        self.grid[gr][gc] = 0

        self.running = True
        self.game_over = False

    def _generate_grid(self, density):
        grid = [[0 for _ in range(self.width_cells)] for _ in range(self.height_cells)]
        for r in range(self.height_cells):
            for c in range(self.width_cells):
                if random.random() < density:
                    grid[r][c] = 1
        return grid

    def update(self):
        if self.game_over:
            return

        # Check win condition (all agents finished)
        if all(agent.finished for agent in self.agents):
            self.game_over = True
            status = " | ".join([f"{agent.name}: {agent.steps}" for agent in self.agents])
            print(f"Race Over! {status}")
            return

        for agent in self.agents:
            if not agent.finished:
                if agent.pos == self.goal:
                    agent.finished = True
                else:
                    # Calculate move considering other agents as obstacles
                    other_agents = [a for a in self.agents if a != agent]
                    next_pos = agent.get_next_move(self.grid, self.goal, other_agents)
                    agent.pos = next_pos
                    agent.path_history.append(next_pos)
                    agent.steps += 1

    def draw(self):
        self.screen.fill(COLOR_BG)

        # Draw Grid & Walls
        for r in range(self.height_cells):
            for c in range(self.width_cells):
                rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, COLOR_GRID, rect, 1) # Grid lines
                
                if self.grid[r][c] == 1:
                    pygame.draw.rect(self.screen, COLOR_WALL, rect)

        # Draw Goal
        gr, gc = self.goal
        goal_rect = pygame.Rect(gc * CELL_SIZE, gr * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, COLOR_GOAL, goal_rect)
        
        # Draw Trails (History)
        for agent in self.agents:
            for r, c in agent.path_history:
                center = (c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2)
                pygame.draw.circle(self.screen, COLOR_TRAIL, center, 2)

        # Draw Agents
        for agent in self.agents:
            ar, ac = agent.pos
            center = (ac * CELL_SIZE + CELL_SIZE // 2, ar * CELL_SIZE + CELL_SIZE // 2)
            pygame.draw.circle(self.screen, agent.color, center, CELL_SIZE // 2 - 4)

        # Draw UI Text
        if self.game_over:
            status_text = " | ".join([f"{a.name}: {a.steps}" for a in self.agents])
            text_surf = self.font.render(status_text, True, COLOR_TEXT)
            # Draw text background for readability
            bg_rect = text_surf.get_rect(center=(self.screen_w // 2, self.screen_h // 2))
            bg_rect.inflate_ip(20, 20)
            pygame.draw.rect(self.screen, (0, 0, 0), bg_rect)
            pygame.draw.rect(self.screen, COLOR_TEXT, bg_rect, 2)
            self.screen.blit(text_surf, text_surf.get_rect(center=(self.screen_w // 2, self.screen_h // 2)))

        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if event.key == pygame.K_r: # Restart
                        # Re-init with same agents? No, need to reset agents.
                        # For simplicity, just quit or we'd need to reset agents' state.
                        # Let's just re-create the sim in main loop if we wanted full restart, 
                        # but here we'll just close for now or maybe reset agents.
                        # To properly restart, we need to reset agents to start pos.
                        pass 

            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()