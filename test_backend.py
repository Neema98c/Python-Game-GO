from board import Board

b = Board(size=9)

b.play_move(2, 2, Board.BLACK)
b.play_move(3, 2, Board.WHITE)
b.print_board()