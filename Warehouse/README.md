# Warehouse Simulation: BFS vs A\* Pathfinding

## Problem Overview

This project simulates a warehouse environment where autonomous agents must navigate a grid filled with static obstacles (walls) and dynamic obstacles (other agents) to reach a specific goal. The core problem is **pathfinding**: finding an optimal or feasible path from a starting position to a target destination in a grid-based map.

The simulation visually demonstrates the difference in behavior and efficiency between two fundamental graph traversal algorithms: **Breadth-First Search (BFS)** and **A\* (A-Star) Search**.

## Methods Used

### 1. Breadth-First Search (BFS)

**What it is:** BFS is an algorithm for traversing or searching tree or graph data structures. It starts at the tree root (or some arbitrary node of a graph) and explores all of the neighbor nodes at the present depth prior to moving on to the nodes at the next depth level.

**Why we use it:**

- **Optimality:** In an unweighted graph (like our grid where every step costs 1), BFS guarantees finding the **shortest path** (minimum number of steps) to the goal.
- **Completeness:** If a path exists, BFS will find it.
- **Simplicity:** It serves as a perfect baseline to compare against more complex algorithms.

### 2. A\* (A-Star) Search

**What it is:** A\* is a graph traversal and path search algorithm, which is often used in many fields of computer science due to its completeness, optimality, and optimal efficiency. It uses a heuristic to guide the search.

**Why we use it:**

- **Efficiency:** Unlike BFS which explores blindly in all directions, A\* uses a **heuristic function** (Manhattan Distance in this case) to estimate the cost to the goal. This allows it to prioritize paths that seem more promising, often finding the goal much faster (visiting fewer nodes) than BFS.
- **Goal-Directed:** It is specifically designed for finding the shortest path to a specific goal node, making it ideal for agent navigation.

## Code Structure & Key Components

### 1. `WarehouseSim.py`

This file handles the core simulation loop and visualization.

- **`WarehouseSim` Class**:
  - **`__init__`**: Sets up the Pygame window, grid, and agents.
  - **`_generate_grid(density)`**: Creates a randomized grid where `1` represents a wall and `0` represents empty space.
  - **`update()`**: The main logic loop. It checks for win conditions and iterates through agents to trigger their movement.
  - **`draw()`**: Renders the grid, walls, agents, trails, and UI text to the screen.

### 2. `Agent.py`

Defines the base behavior for all agents.

- **`Agent` Class**:
  - **`get_next_move(grid, goal, other_agents)`**: Abstract method that must be implemented by subclasses.
  - **`get_neighbors(node, grid, dynamic_obstacles)`**: A utility function that returns valid adjacent cells (up, down, left, right).
    - **Logic**: It checks boundaries, static walls (`grid[r][c] == 0`), and dynamic obstacles (positions of other agents). This prevents agents from walking into walls or each other.

### 3. `main.py`

Contains the specific algorithm implementations and the entry point.

- **`BFSAgent` Class**:

  - **`get_next_move`**: Implements the BFS algorithm.
    - **Logic**: Uses a queue (`collections.deque`) to store paths. It explores layer by layer until the `goal` is found. The first step of the found path is returned as the next move.

- **`AStarAgent` Class**:
  - **`heuristic(a, b)`**: Calculates the **Manhattan Distance** (`|x1 - x2| + |y1 - y2|`) between the current node and the goal. This heuristic is admissible for a grid, ensuring the shortest path is found.
  - **`get_next_move`**: Implements the A\* algorithm.
    - **Logic**: Uses a priority queue (`heapq`) to store paths based on their `f_score` (`g_score + heuristic`). `g_score` is the cost from start, and `f_score` is the estimated total cost. This ensures the agent always expands the most promising node first.

### 4. `config.py`

A central place for configuration constants like `GRID_WIDTH`, `GRID_HEIGHT`, `FPS`, and colors. This makes it easy to tweak the simulation parameters without diving into the logic code.

## How to Run

Execute the `main.py` file to start the simulation:

```bash
python main.py
```
