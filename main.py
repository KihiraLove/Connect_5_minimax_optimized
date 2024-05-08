from board import Board
from bot import Bot

board = Board()
bot = Bot(board)
win = False
isPlayerX = True
enlarged = False
last_move = ()
while not win:
    board.print_board()
    try:
        if isPlayerX:
            move = input("Enter your move (x y): ").split(' ')
            x = int(move[0])
            y = int(move[1])
            last_move = (x, y)
            win, enlarged = board.move(x, y, isPlayerX)
        else:
            move = bot.smart_move(last_move, enlarged)
            win, enlarged = board.move(move[0], move[1], isPlayerX)
        isPlayerX = not isPlayerX
    except IndexError:
        print("Invalid move")


