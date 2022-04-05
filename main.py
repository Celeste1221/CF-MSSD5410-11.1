# original code taken from:
# https://www.geeksforgeeks.org/tic-tac-toe-gui-in-python-using-pygame/
# accessed on 3/24/22
# attributed to : AbhijitTripathy
# license not specified

# CHANGELOG:
# changed MOUSEBUTTONDOWN test from is to ==
# added flush after filling the screen with white
# incorporated Minimax algorithm
# made this a computer against computer game

# importing the required libraries
import pygame as pg
import sys
import time
import random
from pygame.locals import *

# declaring the global variables

draw = None
ran = 0
mmx = 0
draws = 0

# for storing the 'x' or 'o'
# value as character
XO = 'X'
# initial values of alpha and beta
MAX, MIN = 1000, -1000

# storing the winner's value at
# any instant of code
winner = ""

# to set width of the game window
width = 400

# to set height of the game window
height = 400

# to set background color of the
# game window
white = (255, 255, 255)

# color of the straightlines on that
# white game board, dividing board
# into 9 parts
line_color = (0, 0, 0)

# setting up a 3 * 3 board in canvas
board = [[None] * 3, [None] * 3, [None] * 3]

# initializing the pygame window
pg.init()

# setting fps manually
fps = 30

# this is used to track time
CLOCK = pg.time.Clock()

# this method is used to build the
# infrastructure of the display
screen = pg.display.set_mode((width, height + 100), 0, 32)

# setting up a nametag for the
# game window
pg.display.set_caption("My Tic Tac Toe")

# loading the images as python object
initiating_window = pg.image.load("modified_cover.png")
x_img = pg.image.load("X_modified.png")
y_img = pg.image.load("o_modified.png")

# resizing images
initiating_window = pg.transform.scale(initiating_window, (width, height + 100))
x_img = pg.transform.scale(x_img, (80, 80))
o_img = pg.transform.scale(y_img, (80, 80))


def game_initiating_window():
    # displaying over the screen
    screen.blit(initiating_window, (0, 0))

    # updating the display
    pg.display.update()
    time.sleep(0.1)
    screen.fill(white)

    # flush old events from menu
    pg.event.clear()

    # drawing vertical lines
    pg.draw.line(screen, line_color, (width / 3, 0), (width / 3, height), 7)
    pg.draw.line(screen, line_color, (width / 3 * 2, 0), (width / 3 * 2, height), 7)

    # drawing horizontal lines
    pg.draw.line(screen, line_color, (0, height / 3), (width, height / 3), 7)
    pg.draw.line(screen, line_color, (0, height / 3 * 2), (width, height / 3 * 2), 7)
    draw_status()


def draw_status():
    global draw, ran, mmx, draws

    if winner is None:
        message = XO.upper() + "'s Turn"
    else:
        if winner == 'X':
            ran += 1
        else:
            mmx += 1
        message = winner.upper() + " won!"
    if draw:
        draws += 1
        message = "Game Draw!"

        # setting a font object
    font = pg.font.Font(None, 30)

    # setting the font properties like
    # color and width of the text
    text = font.render(message, True, (255, 255, 255))

    # copy the rendered message onto the board
    # creating a small block at the bottom of the main display
    screen.fill((0, 0, 0), (0, 400, 500, 100))
    text_rect = text.get_rect(center=(width / 2, 500 - 50))
    screen.blit(text, text_rect)
    pg.display.update()


def check_win(ret_val=False):
    global board, winner, draw

    # draw is what the ret_val cares about
    # moved these lines up from the bottom

    if all([all(row) for row in board]) and winner is None:
        draw = True

    if ret_val:
        if draw:
            draw = None
            return True
        else:
            return False

    # checking for winning rows
    for row in range(0, 3):
        if (board[row][0] == board[row][1] == board[row][2]) and (board[row][0] is not None):
            winner = board[row][0]
            pg.draw.line(screen, (250, 0, 0),
                         (0, (row + 1) * height / 3 - height / 6),
                         (width, (row + 1) * height / 3 - height / 6),
                         4)
            break

    # checking for winning columns
    for col in range(0, 3):
        if (board[0][col] == board[1][col] == board[2][col]) and (board[0][col] is not None):
            winner = board[0][col]
            pg.draw.line(screen, (250, 0, 0), ((col + 1) * width / 3 - width / 6, 0),
                         ((col + 1) * width / 3 - width / 6, height), 4)
            break

    # check for diagonal winners
    if (board[0][0] == board[1][1] == board[2][2]) and (board[0][0] is not None):
        # game won diagonally left to right
        winner = board[0][0]
        pg.draw.line(screen, (250, 70, 70), (50, 50), (350, 350), 4)

    if (board[0][2] == board[1][1] == board[2][0]) and (board[0][2] is not None):
        # game won diagonally right to left
        winner = board[0][2]
        pg.draw.line(screen, (250, 70, 70), (350, 50), (50, 350), 4)

    draw_status()


def drawXO(row, col):
    global board, XO

    # for the first row, the image
    # should be pasted at a x coordinate
    # of 30 from the left margin
    if row == 1:
        posx = 30

    # for the second row, the image
    # should be pasted at a x coordinate
    # of 30 from the game line
    if row == 2:
        # margin or width / 3 + 30 from
        # the left margin of the window
        posx = width / 3 + 30

    if row == 3:
        posx = width / 3 * 2 + 30

    if col == 1:
        posy = 30

    if col == 2:
        posy = height / 3 + 30

    if col == 3:
        posy = height / 3 * 2 + 30

    # setting up the required board
    # value to display
    board[row - 1][col - 1] = XO

    if XO == 'X':

        # pasting x_img over the screen
        # at a coordinate position of
        # (pos_y, posx) defined in the
        # above code
        screen.blit(x_img, (posy, posx))
        XO = 'O'

    else:
        screen.blit(o_img, (posy, posx))
        XO = 'X'
    pg.display.update()


def user_click():
    # get coordinates of mouse click
    x, y = pg.mouse.get_pos()

    # get column of mouse click (1-3)
    if x < width / 3:
        col = 1

    elif x < width / 3 * 2:
        col = 2

    elif x < width:
        col = 3

    else:
        col = None

    # get row of mouse click (1-3)
    if y < height / 3:
        row = 1

    elif y < height / 3 * 2:
        row = 2

    elif y < height:
        row = 3

    else:
        row = None

    # after getting the row and col,
    # we need to draw the images at
    # the desired positions
    if row and col and board[row - 1][col - 1] is None:
        global XO
        drawXO(row, col)
        check_win()
        if not check_win(True):
            # computer only moves if click was valid and game not over
            computer_move()


def evaluate(b):
    player = 'O'
    opponent = 'X'
    for row in range(0, 3):
        if b[row][0] == b[row][1] and b[row][1] == b[row][2]:
            if b[row][0] == player:
                return +10
            elif b[row][0] == opponent:
                return -10
    for col in range(0, 3):
        if b[0][col] == b[1][col] and b[1][col] == b[2][col]:
            if b[0][col] == player:
                return +10
            elif b[0][col] == opponent:
                return -10
    # checking for diagonals for X or O victory
    if b[0][0] == b[1][1] and b[1][1] == b[2][2]:
        if b[0][0] == player:
            return +10
        elif b[0][0] == opponent:
            return -10

    if b[0][2] == b[1][1] and b[1][1] == b[2][0]:
        if b[0][2] == player:
            return +10
        elif b[0][2] == opponent:
            return -10

    # else if none of them have won, return 0
    return 0


# tried to minimize repeat code - this function not working
def make_move(MIN_MAX, player, depth, is_max, alpha, beta):
    best = MIN_MAX
    # traverse all cells, evaluate minimax function for all empty cells and return the cell with optimal value
    for row in range(1, 4):
        for col in range(1, 4):
            # check if cell is empty and valid
            if board[row - 1][col - 1] is None:
                # make the move
                board[row - 1][col - 1] = player
                # compute evaluation function for this move
                val = minimax(board, depth + 1, not is_max, alpha, beta)
                print("Min_max: " + str(MIN_MAX))
                print("val: " + str(val))
                print("best: " + str(best))
                if player == 'O':  # maximizer's turn
                    best = max(best, val)
                    print("O best: " + str(best))
                    alpha = max(alpha, best)
                    print("alpha: " + str(alpha))
                elif player == 'X':  # minimizer's turn
                    best = min(best, val)
                    beta = min(beta, best)
                    print("X best: " + str(best))

                # undo the move
                board[row - 1][col - 1] = None

                # prune further steps if necessary
                if beta <= alpha:
                    # since it is a nested loop, return
                    return best
    return best


def minimax(board, depth, is_max, alpha, beta):
    score = evaluate(board)

    # either max won with 10 or min with -10
    if abs(score) == 10:
        return score

    # if this board would be a draw
    if check_win(True):
        return 0

    # if it is maximizer's turn
    if is_max:
        # make_move function doesn't work
        # make_move(MIN, 'O', depth+1, not is_max, alpha, beta)  # returns best move

        # repeat code from computer_move. can clean this later
        best = MIN

        # traverse all cells, evaluate minimax function for all empty cells and return cell with optimal value
        for row in range(1, 4):
            for col in range(1, 4):
                # check if cell is empty and valid
                if board[row - 1][col - 1] is None:
                    # make the move
                    board[row - 1][col - 1] = 'O'
                    # compute evaluation function for this move, implement minimax
                    val = minimax(board, depth + 1, not is_max, alpha, beta)
                    best = max(best, val)
                    alpha = max(alpha, best)
                    # undo the move
                    board[row - 1][col - 1] = None

                    # prune further steps if necessary
                    if beta <= alpha:
                        return best
        return best

    # else it is minimizer's turn
    else:
        # make_move(MAX, 'X', depth+1, not is_max, alpha, beta)

        # repeat code from computer_move, except positive score
        best = MAX

        # traverse all cells, evaluate minimax function for all empty cells and return the cell with optimal value
        for row in range(1, 4):
            for col in range(1, 4):
                # check if cell is empty and valid
                if board[row - 1][col - 1] is None:
                    # make the move
                    board[row - 1][col - 1] = 'X'
                    # compute evaluation function for this move
                    val = minimax(board, depth + 1, not is_max, alpha, beta)
                    best = min(best, val)
                    beta = min(beta, best)
                    # undo the move
                    board[row - 1][col - 1] = None

                    # prune further steps if necessary
                    if beta <= alpha:
                        # since it is a nested loop, return
                        return best
        return best


def random_move():
    while True:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if row and col and board[row - 1][col - 1] is None:
            global XO
            drawXO(row, col)
            check_win()
            break


# this will return the best possible move for the player
def computer_move():
    best_val = MIN
    best_move = (-1, -1)

    # traverse all cells, evaluate minimax function for all empty cells, return the cell with optimal value
    for row in range(1, 4):
        for col in range(1, 4):
            # check if cell is empty and valid
            if board[row - 1][col - 1] is None:
                # make the move
                board[row - 1][col - 1] = 'O'
                # compute evaluation function for this move
                # Implement minimax
                move_val = minimax(board, 0, False, MIN, MAX)
                # undo the move
                board[row - 1][col - 1] = None

                # if the value of the current move is more than the best value, then update best
                if move_val > best_val:
                    best_move = (row, col)
                    best_val = move_val
    # perform move with the largest value
    drawXO(best_move[0], best_move[1])
    check_win()


# end def computer_move()

def reset_game():
    global board, winner, XO, draw
    time.sleep(.1)
    XO = 'X'
    draw = False
    game_initiating_window()
    winner = None
    board = [[None] * 3, [None] * 3, [None] * 3]


def main():
    game_initiating_window()
    num_games = 0

    while num_games < 10:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:  # user click
                # user_click()
                print("Draws: {0}, Minimax: {1}, Random: {2}, Games played: {3}".format(draws, mmx, ran, num_games))
                pg.quit()
                sys.exit()

        # time to wait between move pairs
        time.sleep(0.05)
        random_move()  # make a random move
        if winner or draw:  # check for end before next move
            reset_game()
            num_games += 1
        else:
            computer_move()  # minimax move
            if winner or draw:
                reset_game()
                num_games += 1
        pg.display.update()
        CLOCK.tick(fps)
    print("Draws: {0}, Minimax: {1}, Random: {2}, Games played: {3}".format(draws, mmx, ran, num_games))


if __name__ == "__main__":
    main()
