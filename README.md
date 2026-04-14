# AI Algorithm Simulator

A Pygame-based grid navigation project that demonstrates multiple search strategies for moving an agent across a 2D grid while avoiding barriers and completing tasks.

The repository now contains three simulation variants:

- BFS Greedy Nearest Task Search
- A* Search
- Iterative Deepening A* (IDA*)

## Project Overview

Each simulation places an agent on a grid with randomly generated tasks and barriers. The agent starts at the top-left corner and uses a different search strategy depending on the simulation folder.

The simulations are designed to show how algorithm choice affects pathfinding behavior, task completion, and decision-making in a constrained environment.

## Folder Structure

- `BFS_Greedy_Nearest/` - nearest-task selection using BFS shortest-path search
- `A_Star_Algorithm/` - A* pathfinding with a Manhattan distance heuristic
- `IDA_Star_Algorithm/` - IDA* pathfinding with iterative deepening and heuristic pruning

Each folder contains the same core files:

- `agent.py` - agent behavior and pathfinding logic
- `environment.py` - grid generation, tasks, and barriers
- `run.py` - Pygame UI and simulation loop

## Algorithms Used

### BFS Greedy Nearest Task Search

This version uses Breadth-First Search to find paths to available tasks and selects the task with the shortest path first. It is a simple and reliable shortest-path approach on an unweighted grid.

### A* Search

This version uses the A* algorithm with Manhattan distance as the heuristic. It balances the cost already traveled with an estimate of the remaining distance to the target, which usually makes it faster than BFS for pathfinding to a single goal.

### IDA*

This version uses Iterative Deepening A* (IDA*). It combines heuristic guidance with depth-first search style iteration, increasing the search threshold gradually. This uses less memory than A* while still using the heuristic to guide the search.

## Requirements

- Python 3.13 or compatible Python 3 version
- Pygame

## Installation

If Pygame is not installed, install it with:

```bash
pip install pygame
```

If you are using a virtual environment, activate it first before installing dependencies.

## How to Run

Open a terminal in the simulation folder you want to test and run:

```bash
python run.py
```

Examples:

```bash
cd BFS_Greedy_Nearest
python run.py
```

```bash
cd A_Star_Algorithm
python run.py
```

```bash
cd IDA_Star_Algorithm
python run.py
```

## What You Will See

- A grid with randomly placed tasks
- Random barriers that block movement
- A blue agent that moves according to the selected algorithm
- A status panel showing task completion and agent position

## Notes

- The start button begins the simulation in each version.
- The agent only moves through valid grid cells and never crosses barriers.
- You can adjust the number of tasks and barriers in each `run.py` file to make the simulation easier or harder.

## License

See the `LICENSE` file for license information.
