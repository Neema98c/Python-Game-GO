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
        """AI plays a random legal move."""
        if self.game_over or self.current_player != self.bot_color:
            return False, "Not AI's turn or game over."

        legal_moves = []
        for y in range(self.size):
            for x in range(self.size):
                if self.board.get(x, y) != Board.EMPTY:
                    continue
                if self.board.is_suicide(x, y, self.bot_color):
                    continue
                # Ko check already handled in play_move
                legal_moves.append((x, y))

        if not legal_moves:
            return self.pass_turn()  # AI passes if no moves available

        move = random.choice(legal_moves)
        success, msg = self.play_move(move[0], move[1])
        return success, f"AI plays at ({move[0]+1}, {move[1]+1})"