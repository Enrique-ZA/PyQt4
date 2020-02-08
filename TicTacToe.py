'''
# TicTacToe in PyQt4
# Author: Enrique Nelson
# 62746405@mylife.unisa.ac.za
# https://github.com/Enrique-ZA
'''

import sys
import random
import math
from PyQt4 import QtGui, QtCore

# application variables - start
width, height = 500, 500 # main window width, height

cols, rows = 3, 3 # cols and rows
available_spots = cols * rows # calculate available spots
local_available_spots = None
buttonSize = width / cols # size of a button
game_board = [
             ['','',''],
             ['','',''],
             ['','',''],
             ] # game board

# players
human = 'O'
ai = 'X'
current_player = ai # the starting player
# this program is set so that the ai always goes first and is
# the maximizing player
result = None # keep track of game result
isFirstTurn = True # boolean to check if it is the first turn of the game
# application variables - end

app = QtGui.QApplication(sys.argv) # declare app

# User screen dimensions
screen_resolution = app.desktop().screenGeometry()
s_width, s_height = screen_resolution.width(), screen_resolution.height()

window = QtGui.QWidget() # declare main window

# Start application in center of the users screen:
window.setGeometry((s_width/2)-(width/2), (s_height/2)-(height/2), width, height)

window.setWindowTitle("Tic Tac Toe") # main window title

window.setFixedSize(window.size()) #set fixed window size
window.show() # display main window

# functions - start
def reset_game():
    # function resets the game
    global buttons, available_spots, cols, rows, game_board, human, ai, current_player, result, isFirstTurn, local_available_spots
    available_spots = cols * rows
    local_available_spots = None
    game_board = [
                ['','',''],
                ['','',''],
                ['','',''],
                ]

    human = 'O'
    ai = 'X'
    current_player = ai
    result = None
    isFirstTurn = True
    for i in range(available_spots):
        buttons[i].button.setText(" ") # change button text
    ai_move(current_player) # ai goes first


def show_result():
    # function displays the result
    global window, result
    choice = None
    # display result
    # using QtGui.QMessageBox.information works too
    # but makes a windows alert sound while question is silent
    if(result == 'tie'):
        choice = QtGui.QMessageBox.question(window,'Game Over!',
                                                    'The game ended in a ' + str(result) + '!', QtGui.QMessageBox.Ok)
    elif(result == 'X'):
        choice = QtGui.QMessageBox.question(window,'Game Over!',
                                                    'The winner is ' + str(result) + '!', QtGui.QMessageBox.Ok)
    elif(result == 'O'):
        choice = QtGui.QMessageBox.question(window,'Game Over!',
                                                    'The winner is ' + str(result) + '!', QtGui.QMessageBox.Ok)
    if choice == QtGui.QMessageBox.Ok:
        choice = None
        reset_game() # reset game

def check_winner(board):
    # function checks whether there is winner or tie
    global available_spots  
    winner = None

    # columns
    for i in range(3):
        if(board[i][0] == board[i][1] == board[i][2] and board[i][0] == 'X'):
            winner = board[i][0]
        elif(board[i][0] == board[i][1] == board[i][2] and board[i][0] == 'O'):
            winner = board[i][0]

    # rows
    for i in range(3):
        if(board[0][i] == board[1][i] == board[2][i] and board[0][i] == 'X'):
            winner = board[0][i]
        elif(board[0][i] == board[1][i] == board[2][i] and board[0][i] == 'O'):
            winner = board[0][i]

    # diagonals
    if(board[0][0] == board[1][1] == board[2][2] and board[0][0] == 'X'):
        winner = board[0][0]
    elif(board[0][0] == board[1][1] == board[2][2] and board[0][0] == 'O'):
        winner = board[0][0]

    if(board[0][2] == board[1][1] == board[2][0] and board[0][2] == 'X'):
        winner = board[0][2]
    elif(board[0][2] == board[1][1] == board[2][0] and board[0][2] == 'O'):
        winner = board[0][2]

    # tie
    if(winner == None and available_spots == 0):
        return 'tie' # return tie
    else: # returns 'X', 'O' or None
        return winner # return winner

def update_game_board(board):
    # function updates button text
    global cols, rows, buttons
    for i in range(cols):
        for j in range(rows):
            index = j * cols + i # row * cols + col, 2D to 1D index
            buttons[index].button.setText(board[i][j]) # change button text

def mini_max(board, depth, alpha, beta, isMax):
    # minimax function to determine best move
    global ai, human, available_spots, local_available_spots
    r = check_winner(board) # check winner
    if(depth == 0):
        local_available_spots = available_spots - 1 # local variable so that the global is not changed
    else:
        local_available_spots -= 1
    scores = {'X': 10, 'O': -10, 'tie': 0} # dictionary with scores

    # apply score if there is a winner or tie - start
    if(r != None):        
        if(depth == 0):
            score = scores[r]
        else:
            score = (scores[r]/depth)
        return score

    # this is a tied game state
    if(r == None and local_available_spots == 0):
        if(depth == 0):
            score = scores['tie']
        else:
            score = (scores['tie']/depth)
        return score
    # apply score if there is a winner or tie - end

    if(isMax): # maximizing player
        best_score = -math.inf
        for i in range(cols):
            for j in range(rows):
                if(board[i][j] != 'X' and board[i][j] != 'O'):
                    board[i][j] = ai
                    score = mini_max(board, depth + 1, alpha, beta, False)
                    board[i][j] = ' '
                    if(score > best_score):
                        best_score = score
                    alpha = max(alpha, score)
                    if (beta <= alpha):
                        break
        return best_score
    else: # minimizing player
        best_score = math.inf
        for i in range(cols):
            for j in range(rows):
                if(board[i][j] != 'X' and board[i][j] != 'O'):
                    board[i][j] = human
                    score = mini_max(board, depth + 1, alpha, beta, True)
                    board[i][j] = ' '
                    if(score < best_score):
                        best_score = score
                    beta = min(beta, score)
                    if (beta <= alpha):
                        break
        return best_score

def ai_move(c_player):
    global cols, rows, buttons, current_player, game_board, available_spots, result, isFirstTurn
    best_score = -math.inf
    best_i = None
    best_j = None
    if(not isFirstTurn):
        for i in range(cols):
            for j in range(rows):
                if(game_board[i][j] != 'X' and game_board[i][j] != 'O'):
                        # minimax
                        game_board[i][j] = c_player
                        score = mini_max(game_board, 0, -math.inf, math.inf, False)
                        game_board[i][j] = ' '
                        # set best move
                        if(score > best_score):
                            best_score = score
                            best_i = i
                            best_j = j
    else: # randomly select first move
        best_i = math.floor(3 * random.random() + 0)
        best_j = math.floor(3 * random.random() + 0)
        isFirstTurn = False

    game_board[best_i][best_j] = c_player #play move

    update_game_board(game_board) # update game
    available_spots -= 1 # decrease spots available
    result = check_winner(game_board) # check if there is a winner
    # if there is not a winner keep playing, else show result
    if(result == None):
        if(c_player == 'X'):
            current_player = 'O'
        else:
            current_player = 'X'  
    else:
        show_result()
# functions - end

class Button:
    def __init__(self, x, y, i, j):
        global cols, rows, width, height, result
        self.x = x # x position on main window
        self.y = y # y position on main window
        self.colIndex = j # board i/col index
        self.rowIndex = i # board j/row index
        self.button = QtGui.QPushButton(" ", window) # create and attach button to main window    
        self.button.setStyleSheet("font: bold 100px") # button font style
        self.button.btn_width, self.button.btn_height = width/cols, height/rows # button width and height
        if(result == None):
            self.button.clicked.connect(self.player_move) # link click event to function
        else:
            self.button.clicked.connect(show_result) # link click event to function
        self.button.resize(self.button.btn_width,self.button.btn_height) # set button size
        self.button.move(self.x, self.y) # position button to center of main window
        self.button.show()

    def player_move(self):
        global current_player, available_spots, game_board, result
        if(result == None):
            # check if the button may be pressed
            if(current_player == 'O'):
                if(available_spots > 0):
                    if(self.button.text() != 'X' and self.button.text() != 'O'):
                        # set board to player
                        game_board[self.colIndex][self.rowIndex] = current_player
                        update_game_board(game_board) # update game
                        available_spots -= 1 # decrease spots available
                        # check if there is a winner
                        result = check_winner(game_board)
                        # if not keep play, else show result
                        if(result == None):
                            if(current_player == 'X'):
                                current_player = 'O'
                            else:
                                current_player = 'X'                    
                                ai_move(current_player)
                        else:
                            show_result()   

buttons = []

for i in range(cols):
    for j in range(rows):
        buttons.append(Button(i * buttonSize, j * buttonSize, i, j)) # create buttons

ai_move(current_player) # ai goes first

sys.exit(app.exec_()) # keep application open
