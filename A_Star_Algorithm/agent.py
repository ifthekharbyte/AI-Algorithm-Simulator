# agent.py - A* Algorithm Implementation
import pygame
import heapq

class Agent(pygame.sprite.Sprite):
    def __init__(self, environment, grid_size):
        super().__init__()
        self.image = pygame.Surface((grid_size, grid_size))
        self.image.fill((0, 0, 255))  # Agent color is blue
        self.rect = self.image.get_rect()
        self.grid_size = grid_size
        self.environment = environment
        self.position = [0, 0]  # Starting at the top-left corner of the grid
        self.rect.topleft = (0, 0)
        self.task_completed = 0
        self.completed_tasks = []
        self.path = []  # List of positions to follow
        self.moving = False  # Flag to indicate if the agent is moving

    def move(self):
        """Move the agent along the path."""
        if self.path:
            next_position = self.path.pop(0)
            self.position = list(next_position)
            self.rect.topleft = (self.position[0] * self.grid_size, self.position[1] * self.grid_size)
            self.check_task_completion()
        else:
            self.moving = False  # Stop moving when path is exhausted

    def check_task_completion(self):
        """Check if the agent has reached a task location."""
        position_tuple = tuple(self.position)
        if position_tuple in self.environment.task_locations:
            task_number = self.environment.task_locations.pop(position_tuple)
            self.task_completed += 1
            self.completed_tasks.append(task_number)

    def heuristic(self, pos, goal):
        """Manhattan distance heuristic."""
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

    def find_nearest_task(self):
        """Find the nearest task based on A* and move towards it."""
        nearest_task = None
        shortest_path = None
        
        for task_position in self.environment.task_locations.keys():
            path = self.find_path_astar(task_position)
            if path:
                if not shortest_path or len(path) < len(shortest_path):
                    shortest_path = path
                    nearest_task = task_position
        
        if shortest_path:
            self.path = shortest_path[1:]  # Exclude the current position
            self.moving = True

    def find_path_astar(self, target):
        """Find a path to the target position using A* algorithm."""
        start = tuple(self.position)
        goal = target
        
        # Priority queue: (f_score, counter, node, path)
        counter = 0
        open_set = [(self.heuristic(start, goal), counter, start, [start])]
        visited = set()
        
        while open_set:
            f_score, _, current, path = heapq.heappop(open_set)
            
            if current in visited:
                continue
            
            visited.add(current)
            
            if current == goal:
                return path
            
            neighbors = self.get_neighbors(current[0], current[1])
            for neighbor in neighbors:
                if neighbor not in visited:
                    g_score = len(path)  # Cost from start
                    h_score = self.heuristic(neighbor, goal)  # Heuristic to goal
                    f_score = g_score + h_score
                    new_path = list(path)
                    new_path.append(neighbor)
                    counter += 1
                    heapq.heappush(open_set, (f_score, counter, neighbor, new_path))
        
        return None  # No path found

    def get_neighbors(self, x, y):
        """Get walkable neighboring positions."""
        neighbors = []
        directions = [("up", (0, -1)), ("down", (0, 1)), ("left", (-1, 0)), ("right", (1, 0))]
        for _, (dx, dy) in directions:
            nx, ny = x + dx, y + dy
            if self.environment.is_within_bounds(nx, ny) and not self.environment.is_barrier(nx, ny):
                neighbors.append((nx, ny))
        return neighbors
