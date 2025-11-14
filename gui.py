import tkinter as tk
from board import Board

class GoGUI:
    def __init__(self, board_size=9):
        from game_manager import GameManager
        self.gm = GameManager(board_size)
        self.board = self.gm.board
        self.size = board_size

        self.window = tk.Tk()
        self.window.title("Go Game")

        # Visual parameters
        self.margin = 30
        self.cell_size = 40
        self.stone_radius = 16

        canvas_size = self.margin * 2 + self.cell_size * (self.size - 1)
        self.canvas = tk.Canvas(self.window, width=canvas_size, height=canvas_size, bg="#DDB88C")
        self.canvas.pack()

        # Label for messages
        self.message_var = tk.StringVar()
        self.message_label = tk.Label(self.window, textvariable=self.message_var, font=("Arial", 14))
        self.message_label.pack()

        self.draw_board()
        self.canvas.bind("<Button-1>", self.handle_click)

    # --------------------------------------------------
    # Drawing functions
    # --------------------------------------------------

    def draw_board(self):
        """Draw the grid and stones."""
        self.canvas.delete("all")

        # Grid lines
        for i in range(self.size):
            x1 = self.margin
            y = self.margin + i * self.cell_size
            x2 = self.margin + self.cell_size * (self.size - 1)
            self.canvas.create_line(x1, y, x2, y)

            x = self.margin + i * self.cell_size
            y1 = self.margin
            y2 = self.margin + self.cell_size * (self.size - 1)
            self.canvas.create_line(x, y1, x, y2)

        # Stones
        for y in range(self.size):
            for x in range(self.size):
                stone = self.board.get(x, y)
                if stone != Board.EMPTY:
                    px = self.margin + x * self.cell_size
                    py = self.margin + y * self.cell_size

                    color = "black" if stone == Board.BLACK else "white"
                    self.canvas.create_oval(
                        px - self.stone_radius, py - self.stone_radius,
                        px + self.stone_radius, py + self.stone_radius,
                        fill=color
                    )

    # --------------------------------------------------
    # Input handling
    # --------------------------------------------------

    def handle_click(self, event):
        """Convert a click to grid coordinates and play the move."""
        x, y = self.pixel_to_coord(event.x, event.y)

        if x is None:
            return  # Click outside board

        success, msg = self.gm.play_move(x, y)
        self.message_var.set(msg)

        if success:
            # Switch player
            self.current_player = Board.WHITE if self.current_player == Board.BLACK else Board.BLACK

        self.draw_board()

    def pixel_to_coord(self, px, py):
        """Convert pixel position to nearest board intersection."""
        # Find nearest grid intersection
        x = round((px - self.margin) / self.cell_size)
        y = round((py - self.margin) / self.cell_size)

        if not (0 <= x < self.size and 0 <= y < self.size):
            return None, None

        return x, y

    # --------------------------------------------------

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    gui = GoGUI(board_size=9)
    gui.run()