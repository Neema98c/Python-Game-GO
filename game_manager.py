from board import Board

class GameManager:
    def __init__(self, size=9):
        self.board = Board(size)
        self.size = size

        # Game state
        self.current_player = Board.BLACK
        self.player_color = Board.BLACK  # default, can be changed
        self.bot_color = Board.WHITE     # unused until AI added

        self.pass_count = 0
        self.game_over = False

    # --------------------------------------------------
    # Turn handling
    # --------------------------------------------------

    def play_move(self, x, y):
        """Handles a move and controls turn switching."""
        if self.game_over:
            return False, "Game is already over."

        success, msg = self.board.play_move(x, y, self.current_player)
        
        if success:
            self.pass_count = 0  # reset pass counter
            self._switch_turn()

        return success, msg

    def _switch_turn(self):
        self.current_player = (
            Board.WHITE if self.current_player == Board.BLACK else Board.BLACK
        )

    # --------------------------------------------------
    # Passing & game end
    # --------------------------------------------------

    def pass_turn(self):
        """Player passes. Game ends after two consecutive passes."""
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
    # Player setup
    # --------------------------------------------------

    def set_player_color(self, color):
        """Choose whether the human plays Black or White."""
        self.player_color = color
        self.bot_color = Board.WHITE if color == Board.BLACK else Board.BLACK
        self.current_player = Board.BLACK  # Black always starts

    # --------------------------------------------------
    # Utility
    # --------------------------------------------------

    @staticmethod
    def color_name(color):
        return "Black" if color == Board.BLACK else "White"

    def restart(self):
        """Reset entire game state."""
        self.board = Board(self.size)
        self.current_player = Board.BLACK
        self.pass_count = 0
        self.game_over = False
        return True, "Game restarted."