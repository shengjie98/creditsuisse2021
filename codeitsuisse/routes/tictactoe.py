import logging
import json
import requests
import sseclient

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

url = "https://cis2021-arena.herokuapp.com/tic-tac-toe/start/"

@app.route('/tic-tac-toe', methods=['POST'])
def get_id():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    battleId = data['battleId']
    endpoint = url + battleId

    stream_response = requests.get(endpoint, stream=True)

    client = sseclient.SSEClient(stream_response)

    # Loop forever (while connection "open")
    for i, event in enumerate(client.events()):
        logging.info(event.data)
        d = json.loads(event.data)
        if i == 0:
            board = createBoard()   
            player = d['youAre']
            if player == 'O':
                to_post = {
                    "action": 'putSymbol',
                    "position": "NW"
                }
                x = requests.post(endpoint, data = to_post)
                updateBoard(board, "NW", player)

        elif d.get('winner'):
            break
        else:
            if d['player'] == player:
                # means we just made a move
                continue
            elif d.get('action') == 'putSymbol':
                action = d['action']
                if validMove(board, action):
                    updateBoard(board, action, d['player'])
                    move = computeMove(board, player)
                    updateBoard(board, move, player)
                    # TODO send post to make move
                    to_post = {
                        "action": 'putSymbol',
                        "position": move
                    }
                    x = requests.post(endpoint, data = to_post)
                else:
                    # TODO flip table
                    to_post = {
                        "action": "(╯°□°)╯︵ ┻━┻"
                    }
                    x = requests.post(endpoint, data = to_post)

    # logging.info("My result :{}".format(result))
    return json.dumps(0)

def createBoard():
    ''' Creates a blank Board for Tic-Tac-Toe
    '''
    positions = ["NW", "N", "NE",
                 "W", "C", "E",
                 "SW", "S", "SE"]
    board = {}
    for position in positions:
        board[position] = " "
    return board
    
def updateBoard(board, position, symbol):
    ''' Updates the Board for Tic-Tac-Toe
    '''
    board[position] = symbol

    
# =========================================================================== #

# Functions for the Human Player 
# (changes not really required)



def validMove(board, move):
    ''' Checks if the Move is valid for the Board
    '''
    if move in board.keys():
        valid = (board[move] == " ")
    else:
        valid = False
    return valid


# =========================================================================== #

# Functions for the Computer Player
# 1. computeMove : Change a single line as stated in the code to switch from randomChoice to smartChoice
# 2. randomChoice : No change is required in this function, as it will anyway choose randomly from available moves.
# 3. smartChoice : No change is required in this function, as it will anyway call minimax with appropriate parameters.
# 4. minimax : This is the primary segment of the code that you will have to write. Think recursion, and check the LAMS.

def computeMove(board, player):
    ''' Computes Move for the Computer Player
    '''
    # print("Computer Player : Move for", player)
    available = [position for position, value in board.items() if value == " "]
    # print("Options:", available)
    
    # Algorithms for the Computer Player
    # Options: randomChoice, smartChoice
    move = smartChoice(board, player, available)      # You may change this to choose the strategy
    return move


def smartChoice(board, player, available):
    ''' Returns a smart choice using an AI algorithm
    '''
    bestScore = float("-inf")     # initialize bestScore
    bestMove = None               # initialize bestMove
    dupBoard = board.copy()       # duplicate board for simulation
    
    for move in available:
        # Simulate the move
        dupBoard[move] = player
        
        # Find score using Minimax algorithm
        score = minimax(board = dupBoard,         # use board's copy
                        maxSymbol = "O",          # maximize for Computer (O)
                        minSymbol = "X",          # minimize for Human (X)
                        depth = 1,                # depth of search tree
                        isMaximizing = False)     # is the next move for O
        
        # Undo the move for simulation
        dupBoard[move] = " "
        
        # Update bestScore if appropriate
        if (score > bestScore):
            bestScore = score
            bestMove = move
    
    # Return the best move
    return bestMove


# Subroutine for executing Minimax Search algorithm
# Complete this function using standard 'recursion'

def minimax(board, maxSymbol, minSymbol, depth, isMaximizing):
    ''' Minimax algorithm for the recursion
    '''
    # Terminal conditions for recursion
    
    if isBoardFull(board) or depth == 0:
        return 0
    elif isWinner(board, 'O'):
        return 1
    elif isWinner(board, 'X'):
        return -1
    # MISSING   # Fill in the missing conditions to stop the recursion
    # You may use the isWinner and isBoardFull functions if you want
    
    # Keep track of scores at this depth
    scores = []
    available = [position for position, value in board.items() if value == " "]
    
    # Go through all available positions
    symbol = 'O' if isMaximizing else 'X'
    for position in available:
        board[position] = symbol
        score = minimax(board, maxSymbol, minSymbol, depth, not isMaximizing)
        scores.append(score)
        board[position] = " "
    # MISSING   # Fill in all the missing pieces in this code segment
        # Simulate the appropriate move
        # Find the score for the move
        # Undo the move for simulation
            
    # Return max or min as per the level
    if isMaximizing:
        return max(scores)
    else:
        return min(scores)
    # MISSING   # Fill in the return logic for recursion as per level
    
    # Remove the following exception when you complete this function
    # raise NotImplementedError


# =========================================================================== #

# Functions for Game Logic
# (changes not really required)

def isWinner(board, player):
    # Check for 3 valid marks denoting a Win
    win = ((board['NW'] == board['N'] == board['NE'] == player) or # Top Row
           (board['W'] == board['C'] == board['E'] == player) or # Middle Row
           (board['SW'] == board['S'] == board['SE'] == player) or # Bottom Row
           (board['NW'] == board['W'] == board['SW'] == player) or # Left Column
           (board['N'] == board['C'] == board['S'] == player) or # Center Column
           (board['NE'] == board['E'] == board['SE'] == player) or # Right Column
           (board['NW'] == board['C'] == board['SE'] == player) or # Diagonal
           (board['NE'] == board['C'] == board['SW'] == player))   # Diagonal      
    return win


def isBoardFull(board):
    available = any(position == " " for position in board.values())
    return (not available)


# =========================================================================== #

# Miscellaneous functions
# (changes not really required)


    
# =========================================================================== #

# Function for the actual Game
# (changes not really required)

# def tictactoe_HC():
#     ''' Gameplay function for Tic-Tac-Toe
#     '''
#     # Introduction
#     printIntro()

#     # Initiate the game
#     gameBoard = createBoard()
#     currentPlayer, nextPlayer = getFirstPlayer("X", "O")
#     printBoard(gameBoard)

#     # Main gameplay loop
#     while True:
#         # Get the move of current Player and update Board
        
#         # If it is turn of the Human Player: Get the Move
#         if currentPlayer == "X":
#             while True:
#                 currentMove = getMove(gameBoard, currentPlayer)
#                 if validMove(gameBoard, currentMove):
#                     updateBoard(gameBoard, currentMove, currentPlayer)
#                     break
#                 else:
#                     print("Sorry, wrong move. Check again.")
                    
#         # If it is turn for the Computer: Compute the Move
#         elif currentPlayer == "O":
#             currentMove = computeMove(gameBoard, currentPlayer)
#             updateBoard(gameBoard, currentMove, currentPlayer)
    
    
#         # Print the updated Board
#         printBoard(gameBoard)
            
#         # Check for terminate-or-continue conditions
#         if isWinner(gameBoard, currentPlayer):
#             # If the current Player Won the game
            
#             # If the current Player is Human
#             if currentPlayer == "X":
#                 print("Congratulations! You have won the game.")
                
#             # If the current Player is Computer
#             elif currentPlayer == "O":
#                 print("Oh well! You just lost to the Computer.")
#             break
            
#         elif isBoardFull(gameBoard):
#             # If the Board is full and it's a Tie
#             print("Wow! This game is a tie. Play again.")
#             break
            
#         else:
#             # Otherwise switch the two Players for next round
#             currentPlayer, nextPlayer = nextPlayer, currentPlayer

#     # Conclusion
#     printFinal()

# # =========================================================================== #

