import random
import copy
from board import Board

class GameManager:
    def __init__(self, size=9):
        self.size = size
        self.board = Board(size)

        # Game state
        self.current_player = Board.BLACK
        self.player_color = Board.BLACK
        self.bot_color = Board.WHITE
        self.pass_count = 0
        self.game_over = False
        self.captured_last_move = 0  # For AI capture detection

    # --------------------------------------------------
    # Turn handling
    # --------------------------------------------------

    def play_move(self, x, y):
        if self.game_over:
            return False, "Game is already over."

        success, msg, captured = self.board.play_move(x, y, self.current_player)
        if success:
            self.captured_last_move = captured
            self.pass_count = 0
            self._switch_turn()
        return success, msg

    def _switch_turn(self):
        self.current_player = (
            Board.WHITE if self.current_player == Board.BLACK else Board.BLACK
        )

    # --------------------------------------------------
    # Passing & resign
    # --------------------------------------------------

    def pass_turn(self):
        if self.game_over:
            return False, "Game is already over."

        self.pass_count += 1
        if self.pass_count >= 2:
            self.game_over = True
            return True, "Both players passed. Game over."

        self._switch_turn()
        return True, f"{self.color_name(self.current_player)} to play."

    def resign(self):
        if self.game_over:
            return False, "Game already over."

        self.game_over = True
        loser = self.color_name(self.current_player)
        winner = self.color_name(Board.WHITE if self.current_player == Board.BLACK else Board.BLACK)
        return True, f"{loser} resigns. {winner} wins."

    # --------------------------------------------------
    # Restart & player color
    # --------------------------------------------------

    def restart(self):
        self.board = Board(self.size)
        self.current_player = Board.BLACK
        self.pass_count = 0
        self.game_over = False
        self.captured_last_move = 0
        return True, "Game restarted."

    def set_player_color(self, color):
        self.player_color = color
        self.bot_color = Board.WHITE if color == Board.BLACK else Board.BLACK
        self.current_player = Board.BLACK  # Black always starts

    # --------------------------------------------------
    # AI logic
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

                # Simulate captures
                captured = self.simulate_captures(x, y, self.bot_color)
                if captured > 0:
                    capture_moves.append((x, y))
                else:
                    legal_moves.append((x, y))

        # -----------------------------
        # Pick a move or pass if none
        # -----------------------------
        if capture_moves:
            move = random.choice(capture_moves)
            success, msg = self.play_move(move[0], move[1])
            return success, f"AI captures at ({move[0]+1},{move[1]+1})"

        elif legal_moves:
            # Prefer moves adjacent to own stones
            adjacent_moves = [m for m in legal_moves if any(
                self.board.get(nx, ny) == self.bot_color
                for nx, ny in self.board.get_neighbors(*m)
            )]
            if adjacent_moves:
                move = random.choice(adjacent_moves)
            else:
                move = random.choice(legal_moves)

            success, msg = self.play_move(move[0], move[1])
            return success, f"AI plays at ({move[0]+1},{move[1]+1})"

        else:
            # No legal moves → pass
            success, msg = self.pass_turn()
            return success, "AI has no legal moves left and passes."

    # --------------------------------------------------
    # Helper functions
    # --------------------------------------------------

    def simulate_captures(self, x, y, color):
        temp_board = copy.deepcopy(self.board)
        success, msg, captured = temp_board.play_move(x, y, color)
        return captured

    @staticmethod
    def color_name(color):
        return "Black" if color == Board.BLACK else "White"