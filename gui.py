import tkinter as tk
from game_manager import GameManager
from board import Board

class GoGUI:
    def __init__(self, board_size=9):
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
        self.message_label.pack(pady=5)

        # Buttons
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=5)

        self.pass_button = tk.Button(button_frame, text="Pass", command=self.pass_turn, width=12)
        self.pass_button.grid(row=0, column=0, padx=5)

        self.resign_button = tk.Button(button_frame, text="Resign", command=self.resign, width=12)
        self.resign_button.grid(row=0, column=1, padx=5)

        self.draw_board()
        self.canvas.bind("<Button-1>", self.handle_click)

    # --------------------------------------------------
    # Drawing functions
    # --------------------------------------------------

    def draw_board(self):
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
    # Move input handling
    # --------------------------------------------------

    def handle_click(self, event):
        """Handle human move and trigger AI if necessary."""
        if self.gm.game_over:
            self.message_var.set("Game over. Restart to play again.")
            return

        # Human move
        x, y = self.pixel_to_coord(event.x, event.y)
        if x is None:
            return

        if self.gm.current_player != self.gm.player_color:
            self.message_var.set("Wait for your turn.")
            return

        success, msg = self.gm.play_move(x, y)
        self.message_var.set(msg)
        self.draw_board()

        # AI move (if it's AI's turn)
        if not self.gm.game_over and self.gm.current_player == self.gm.bot_color:
            self.window.after(500, self.ai_turn)  # delay for visibility

    def ai_turn(self):
        success, msg = self.gm.play_ai_move()
        self.message_var.set(msg)
        self.draw_board()

    def pixel_to_coord(self, px, py):
        x = round((px - self.margin) / self.cell_size)
        y = round((py - self.margin) / self.cell_size)

        if not (0 <= x < self.size and 0 <= y < self.size):
            return None, None

        return x, y

    # --------------------------------------------------
    # Pass & resign buttons
    # --------------------------------------------------

    def pass_turn(self):
        success, msg = self.gm.pass_turn()
        self.message_var.set(msg)
        self.draw_board()

    def resign(self):
        success, msg = self.gm.resign()
        self.message_var.set(msg)
        self.draw_board()

    # --------------------------------------------------

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    gui = GoGUI(board_size=9)
    gui.run()