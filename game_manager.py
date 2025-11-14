import random
from board import Board

class GameManager:
    def __init__(self, size=9):
        self.board = Board(size)
        self.size = size

        self.current_player = Board.BLACK
        self.player_color = Board.BLACK  # Human default
        self.bot_color = Board.WHITE     # AI default

        self.pass_count = 0
        self.game_over = False

    # ... existing methods remain unchanged ...

    # --------------------------------------------------
    # Simple AI logic
    # --------------------------------------------------

    def play_ai_move(self):
        """AI plays a slightly smarter move."""
        if self.game_over or self.current_player != self.bot_color:
            return False, "Not AI's turn or game over."

        legal_moves = []
        capture_moves = []

        for y in range(self.size):
            for x in range(self.size):
                if self.board.get(x, y) != Board.EMPTY:
                    continue
                if self.board.is_suicide(x, y, self.bot_color):
                    continue

                # Simulate the move to check if it captures
                captured = self.board.simulate_captures(x, y, self.bot_color)
                if captured > 0:
                    capture_moves.append((x, y))
                else:
                    legal_moves.append((x, y))

        # 1️⃣ Prefer capturing moves
        if capture_moves:
            move = random.choice(capture_moves)
            success, msg = self.play_move(move[0], move[1])
            return success, f"AI captures at ({move[0]+1},{move[1]+1})"

        # 2️⃣ Prefer moves adjacent to own stones
        adjacent_moves = []
        for move in legal_moves:
            x, y = move
            neighbors = self.board.get_neighbors(x, y)
            if any(self.board.get(nx, ny) == self.bot_color for nx, ny in neighbors):
                adjacent_moves.append(move)

        if adjacent_moves:
            move = random.choice(adjacent_moves)
        else:
            # 3️⃣ Fallback random
            move = random.choice(legal_moves)

        success, msg = self.play_move(move[0], move[1])
        return success, f"AI plays at ({move[0]+1},{move[1]+1})"