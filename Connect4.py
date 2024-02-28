#define the board
import random
import math
import copy

ROW_COUNT = 6
COL_COUNT = 7
EMPTY = ' '
WINDOW_LENGTH = 4

player = 'O'
bot ='X'
board = [[' '] * COL_COUNT for i in range(ROW_COUNT)] #creates a 6x7 matrix of char that stores board


#function to print the board
def printBoard(board):
    for row in range(ROW_COUNT):
        print(board[row])

#function to check if board is draw
def chkDraw(board):
    for row in range(ROW_COUNT):
        for col in range(COL_COUNT):
            if (board[row][col]==' '):
                return False
    return True

#function to check if one user has won
def chkForWin(board):
    #Check horizontal wins
    for c in range(COL_COUNT - 3):#makes sure we stay in bounds. 7-3=4 range(4): 0-3
        for r in range(ROW_COUNT):#Makes sure we go through all rows.
            if board[r][c]==board[r][c+1] and board[r][c]==board[r][c+2] and board[r][c]==board[r][c+3] and board[r][c]!=' ':
                return True
    
    #Check vertical wins
    for c in range(COL_COUNT):#makes sure we go through all columns.
        for r in range(ROW_COUNT-3):#Makes sure we stay in bounds. 6-3=3 range(3): 0-2
            if board[r][c]==board[r+1][c] and board[r][c]==board[r+2][c] and board[r][c]==board[r+3][c] and board[r][c]!=' ':
                return True
    
    #Check negative sloped diagonal wins
    for c in range(COL_COUNT-3):        #makes sure we stay within area at the top left where all
        for r in range(ROW_COUNT-3):    #negative looking sloped diagonal wins can possibly be.
            if board[r][c]==board[r+1][c+1] and board[r][c]==board[r+2][c+2] and board[r][c]==board[r+3][c+3] and board[r][c]!=' ':
                return True
    
    #Check positive sloped diagonal wins
    for c in range(COL_COUNT-3):        #makes sure we stay within area at the bottom left where all
        for r in range(3, ROW_COUNT):    #positive looking sloped diagonal wins can possibly be.
            if board[r][c]==board[r-1][c+1] and board[r][c]==board[r-2][c+2] and board[r][c]==board[r-3][c+3] and board[r][c]!=' ':
                return True
            
    return False
            
#function to check who won
def winningMove(board, mark):
    #Check horizontal wins
    for c in range(COL_COUNT - 3):#makes sure we stay in bounds. 7-3=4 range(4): 0-3
        for r in range(ROW_COUNT):#Makes sure we go through all rows.
            if board[r][c]==board[r][c+1] and board[r][c]==board[r][c+2] and board[r][c]==board[r][c+3] and board[r][c]==mark:
                return True
    
    #Check vertical wins
    for c in range(COL_COUNT):#makes sure we go through all columns.
        for r in range(ROW_COUNT-3):#Makes sure we stay in bounds. 6-3=3 range(3): 0-2
            if board[r][c]==board[r+1][c] and board[r][c]==board[r+2][c] and board[r][c]==board[r+3][c] and board[r][c]==mark:
                return True
    
    #Check negative sloped diagonal wins
    for c in range(COL_COUNT-3):        #makes sure we stay within area at the top left where all
        for r in range(ROW_COUNT-3):    #negative looking sloped diagonal wins can possibly be.
            if board[r][c]==board[r+1][c+1] and board[r][c]==board[r+2][c+2] and board[r][c]==board[r+3][c+3] and board[r][c]==mark:
                return True
    
    #Check positive sloped diagonal wins
    for c in range(COL_COUNT-3):        #makes sure we stay within area at the bottom left where all
        for r in range(3, ROW_COUNT):    #positive looking sloped diagonal wins can possibly be.
            if board[r][c]==board[r-1][c+1] and board[r][c]==board[r-2][c+2] and board[r][c]==board[r-3][c+3] and board[r][c]==mark:
                return True
            
    return False

#gets next open row of a column for a piece to be placed
def getNextOpenRow(board, column):
    for row in range(ROW_COUNT-1, -1, -1):
        if board[row][column] == ' ':
            return row


#function to check is a certain position in the board is empty.       
def isNotFull(board, column):
    for row in range(ROW_COUNT):
        if board[row][column] == ' ':
            return True
    return False 

#simulates placing a mark on the board
def dropMark(board, row, col, mark):
	board[row][col] = mark

#gets all valid columns a mark can be dropped 
def getValidLocations(board):
    validLocations = []
    
    for col in range(COL_COUNT):
        if isNotFull(board, col):
            validLocations.append(col)
    return validLocations

def gameIsOver(board):
    return (winningMove(board, player) or winningMove(board, bot) or len(getValidLocations(board))==0)


def evaluate_window(window, piece):
	score = 0
	opp_piece = player
	if piece == player:
		opp_piece = bot

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 4

	return score

def score_position(board, piece):
	score = 0

	## Score center column
	center_array = [row[COL_COUNT//2] for row in board]
	center_count = center_array.count(piece)
	score += center_count * 3

	## Score Horizontal
	for r in range(ROW_COUNT):
		row_array = [i for i in board[r]]
		for c in range(COL_COUNT-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score Vertical
	for c in range(COL_COUNT):
		col_array = [board[r][c] for r in range(ROW_COUNT)]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score posiive sloped diagonal
	for r in range(ROW_COUNT-3):
		for c in range(COL_COUNT-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	for r in range(ROW_COUNT-3):
		for c in range(COL_COUNT-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	return score

def minimax(board, depth, IsMaximizing):
    validLocations = getValidLocations(board)
    
    if (depth == 0 or gameIsOver(board)):#checks if depth done iterating or game is over
        if(gameIsOver(board)):#checks is the game was either won or lost
            if(winningMove(board, bot)):
                return 100000000000000
            elif(winningMove(board,player)):
                return -100000000000000
            else:#game is draw
                return 0
        else: #else 
            return score_position(board, bot)
    
    if IsMaximizing:
        maxValue = -math.inf
        for col in validLocations:
            row = getNextOpenRow(board, col)
            b_copy = copy.deepcopy(board)
            dropMark(b_copy, row, col, bot)
            maxValue = max(maxValue,minimax(b_copy, depth-1, False))
        return maxValue
    
    else: # Minimizing player
        minValue = math.inf
        for col in validLocations:
            row = getNextOpenRow(board, col)
            b_copy = copy.deepcopy(board)
            dropMark(b_copy, row, col, player)
            minValue = min(minValue,minimax(b_copy, depth-1, True))
        return minValue


#function for player move
def playerMove():
    position=int(input('Enter Column to drop O (1-7):'))-1
    row = getNextOpenRow(board, position)
    if(row is not None):
        dropMark(board, row, position, player)
        printBoard(board)
        print()
    else:
        print("column is full choose a new column")
        playerMove()
    
        
    if winningMove(board, player):
        printBoard(board)
        print("Player Wins!")
        return
    return

#function to get bot to move
def compMove():   
    bestScore=-math.inf #lowest to start with, for comparison to the score after a certain move
    bestCol = random.choice(getValidLocations(board)) #initializing col
    
    #goes through all possible colummn and determines which one is best
    for col in getValidLocations(board):
        temp_board = copy.deepcopy(board)
        row = getNextOpenRow(temp_board, col)
        dropMark(temp_board, row, col, bot)
        score = minimax(temp_board, 5, False)        
        if (score > bestScore):
            bestScore = score
            bestCol = col
    
    #places mark in the column     
    r = getNextOpenRow(board, bestCol)
    dropMark(board, r, bestCol, bot)
    printBoard(board)
    print()
    if winningMove(board, bot):
        printBoard(board)
        print("Bot Wins!")
        print()
        return
    return

    

while not chkForWin(board):
    compMove()
    print()
    playerMove()
    

 