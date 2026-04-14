# agent.py - IDA* Algorithm Implementation
import pygame

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
        """Find the nearest task based on IDA* and move towards it."""
        nearest_task = None
        shortest_path = None
        
        for task_position in self.environment.task_locations.keys():
            path = self.find_path_idstar(task_position)
            if path:
                if not shortest_path or len(path) < len(shortest_path):
                    shortest_path = path
                    nearest_task = task_position
        
        if shortest_path:
            self.path = shortest_path[1:]  # Exclude the current position
            self.moving = True

    def find_path_idstar(self, target):
        """Find a path to the target position using IDA* (Iterative Deepening A*)."""
        start = tuple(self.position)
        goal = target
        
        threshold = self.heuristic(start, goal)
        path = [start]
        
        while True:
            result = self.search_idstar(path, 0, threshold, goal)
            
            if result is True:  # Found the goal
                return path
            
            if result == float('inf'):  # No path exists
                return None
            
            threshold = result

    def search_idstar(self, path, g, threshold, goal):
        """
        Recursive search function for IDA*.
        Returns: True if goal found, new threshold if not found, infinity if no path.
        """
        current = path[-1]
        f = g + self.heuristic(current, goal)
        
        if f > threshold:
            return f
        
        if current == goal:
            return True
        
        min_threshold = float('inf')
        neighbors = self.get_neighbors(current[0], current[1])
        
        for neighbor in neighbors:
            if neighbor not in path:  # Avoid cycles
                path.append(neighbor)
                result = self.search_idstar(path, g + 1, threshold, goal)
                
                if result is True:
                    return True
                
                if result < min_threshold:
                    min_threshold = result
                
                path.pop()  # Backtrack
        
        return min_threshold

    def get_neighbors(self, x, y):
        """Get walkable neighboring positions."""
        neighbors = []
        directions = [("up", (0, -1)), ("down", (0, 1)), ("left", (-1, 0)), ("right", (1, 0))]
        for _, (dx, dy) in directions:
            nx, ny = x + dx, y + dy
            if self.environment.is_within_bounds(nx, ny) and not self.environment.is_barrier(nx, ny):
                neighbors.append((nx, ny))
        return neighbors
