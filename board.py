import copy

class Board:
    EMPTY = 0
    BLACK = 1
    WHITE = 2

    def __init__(self, size=9):
        self.size = size
        self.grid = [[self.EMPTY for _ in range(size)] for _ in range(size)]

    # ---------------------------
    # Move handling
    # ---------------------------
    def play_move(self, x, y, color):
        if self.grid[y][x] != self.EMPTY:
            return False, "Position already occupied.", 0

        # Place stone temporarily
        self.grid[y][x] = color
        captured = 0

        # Check for opponent groups to capture
        for nx, ny in self.get_neighbors(x, y):
            if self.grid[ny][nx] == self.opponent(color):
                if not self.has_liberty(nx, ny):
                    captured += self.remove_group(nx, ny)

        # Check for suicide
        if not self.has_liberty(x, y):
            self.grid[y][x] = self.EMPTY
            return False, "Suicide move not allowed.", 0

        return True, "Move played.", captured

    # ---------------------------
    # Helper functions
    # ---------------------------
    def opponent(self, color):
        return self.BLACK if color == self.WHITE else self.WHITE

    def get(self, x, y):
        return self.grid[y][x]

    def get_neighbors(self, x, y):
        neighbors = []
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                neighbors.append((nx, ny))
        return neighbors

    def has_liberty(self, x, y, visited=None):
        if visited is None:
            visited = set()
        color = self.grid[y][x]
        visited.add((x, y))

        for nx, ny in self.get_neighbors(x, y):
            if self.grid[ny][nx] == self.EMPTY:
                return True
            if self.grid[ny][nx] == color and (nx, ny) not in visited:
                if self.has_liberty(nx, ny, visited):
                    return True
        return False

    def remove_group(self, x, y, color=None, visited=None):
        if visited is None:
            visited = set()
        if color is None:
            color = self.grid[y][x]

        removed = 0
        if (x, y) in visited:
            return 0
        visited.add((x, y))

        if self.grid[y][x] == color:
            self.grid[y][x] = self.EMPTY
            removed += 1
            for nx, ny in self.get_neighbors(x, y):
                removed += self.remove_group(nx, ny, color, visited)
        return removed

    # ---------------------------
    # Utility functions
    # ---------------------------
    def is_suicide(self, x, y, color):
        temp_board = copy.deepcopy(self)
        success, _, _ = temp_board.play_move(x, y, color)
        return not success