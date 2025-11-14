# I plan on making GO using LLM's to demonstrate that I can
# use git effectively. This will be my first commit and 
# will contain only comments outlining my plan.

# The game will need a backend for the game logic, a GUI for the board, 
# a very simple bot to play against and checks to ensure the moves offered are 
# valid.

from copy import deepcopy

class Board:
    EMPTY = 0
    BLACK = 1
    WHITE = 2

    def __init__(self, size=9):
        self.size = size
        self.grid = [[self.EMPTY for _ in range(size)] for _ in range(size)]
        
        # Track last board state for ko rule
        self.previous_state = None  

    def within_bounds(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size

    def get(self, x, y):
        return self.grid[y][x]  # y is row, x is column

    def set(self, x, y, value):
        self.grid[y][x] = value

    # ------------------------------------------------------------
    # GROUP AND LIBERTY LOGIC
    # ------------------------------------------------------------

    def get_neighbors(self, x, y):
        """Return valid orthogonal neighbors."""
        neighbors = []
        for nx, ny in [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]:
            if self.within_bounds(nx, ny):
                neighbors.append((nx, ny))
        return neighbors

    def get_group(self, x, y):
        """Return all stones connected to (x,y)."""
        color = self.get(x, y)
        if color == self.EMPTY:
            return []

        visited = set()
        stack = [(x, y)]
        group = []

        while stack:
            cx, cy = stack.pop()
            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))
            group.append((cx, cy))

            for nx, ny in self.get_neighbors(cx, cy):
                if self.get(nx, ny) == color:
                    stack.append((nx, ny))

        return group

    def count_liberties(self, group):
        """Count distinct liberties for a group of stones."""
        liberties = set()
        for x, y in group:
            for nx, ny in self.get_neighbors(x, y):
                if self.get(nx, ny) == self.EMPTY:
                    liberties.add((nx, ny))
        return len(liberties)

    # ------------------------------------------------------------
    # MOVE VALIDATION AND CAPTURING
    # ------------------------------------------------------------

    def remove_group(self, group):
        for x, y in group:
            self.set(x, y, self.EMPTY)

    def would_capture(self, x, y, color):
        """Returns list of opponent groups to be captured if move is played."""
        opponent = self.BLACK if color == self.WHITE else self.WHITE
        captured = []

        for nx, ny in self.get_neighbors(x, y):
            if self.get(nx, ny) == opponent:
                grp = self.get_group(nx, ny)
                if self.count_liberties(grp) == 1:  # placing here eliminates last liberty
                    captured.append(grp)
        return captured

    def is_suicide(self, x, y, color):
        """Check if move would be suicide (unless it captures something)."""
        test_board = deepcopy(self)
        test_board.set(x, y, color)

        # Check captures first — capturing is allowed even if group has no liberties initially
        opponent_captures = test_board.would_capture(x, y, color)
        for grp in opponent_captures:
            test_board.remove_group(grp)

        group = test_board.get_group(x, y)
        liberties = test_board.count_liberties(group)

        return liberties == 0

    def is_ko(self, new_board_state):
        """Check if new state equals the previous state."""
        return self.previous_state == new_board_state

    # ------------------------------------------------------------
    # MAIN MOVE HANDLER
    # ------------------------------------------------------------

    def play_move(self, x, y, color):
        """
        Attempts to place a stone.
        Returns: (success: bool, error_message: str)
        """
        if not self.within_bounds(x, y):
            return False, "Move outside board."

        if self.get(x, y) != self.EMPTY:
            return False, "Intersection already occupied."

        # Check suicide
        if self.is_suicide(x, y, color):
            return False, "Move is suicidal."

        # Save old state for ko check
        old_state = deepcopy(self.grid)

        # Place stone
        self.set(x, y, color)

        # Capture opponent stones
        captures = self.would_capture(x, y, color)
        for grp in captures:
            self.remove_group(grp)

        # Check ko rule (simple version: must not repeat last state)
        new_state = deepcopy(self.grid)
        if self.is_ko(new_state):
            # Undo move
            self.grid = old_state
            return False, "Ko rule: board position repeating."

        # Store new previous state
        self.previous_state = old_state
        return True, "Move played."

    # ------------------------------------------------------------
    # Debug / Utility
    # ------------------------------------------------------------

    def print_board(self):
        """Text output for debugging."""
        for row in self.grid:
            print(" ".join(str(i) for i in row))
        print()