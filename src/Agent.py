import random
from Board import *
from copy import deepcopy

class Player():
    '''
    Purpose: Class that gives input for interaction between the console player and the TicTacToe board.
    Attributes:
        - pNum: An integer value that represents the player position
            - 1 represents Player 1 (which means an "x" will be played)
            - 2 represents Player 2 (which means an "o" will be played)
    '''
    def __init__(self, pNum):
        self.pNum = pNum

    def __str__(self):
        return "Console Player"

    def get_position(self, board, curRound):
        '''
        Purpose: Takes and converts input from the console into an integer tuple that represents a position to place a token.
        '''
        pos = str(input("Enter a position tuple of the form (x,y):"))
        pos = pos.replace("(", "")
        pos = pos.replace(")", "")
        pos = tuple(int(coordinate) for coordinate in pos.split(","))
        if(pos in board.open_positions()):
            return pos
        else:
            print("The position that was entered is not open for play. The open positions are:")
            print(board.open_positions())
            return self.get_position(board, curRound)

class RandomAgent(Player):
    '''
    Purpose: Benchmark for an agent that chooses a random position that is open for play.
    '''

    def __str__(self):
        return "Random Agent"

    def get_position(self, board, curRound):
        positions = board.open_positions()
        pos = random.choice(positions)
        return pos


class SimpleAgent(Player):

    def __str__(self):
        return "Simple Agent"

    '''
    Purpose: A simple agent that plays by winning if it can, or blocking the opponent if they are in a position to win.
    '''
    def get_position(self, board, curRound):
        winningPositions = board.winning_positions(self.pNum)
        losingPositions = board.losing_positions(self.pNum)
        if(len(winningPositions) > 0):
            return  random.choice(winningPositions)
        elif(len(losingPositions) > 0):
            return random.choice(losingPositions)
        else:
            return random.choice(board.open_positions())



class MiniMaxAgent(Player):

    '''
    Purpose: An agent that uses the minimax algorithm in order to play by searching the game tree.
    '''

    def __str__(self):
        return "MiniMax Agent"

    def value(self, isMaximizing, board):
        if(isMaximizing):
            curPNum = self.pNum
        else:
            curPNum = self.pNum%2+1

        if(isMaximizing):
            if((curPNum == 1 and board.game_state() == -1) or (curPNum == 2 and board.game_state() == 1)):
                return (-1, None)
        if(not isMaximizing):
            if((curPNum == 1 and board.game_state() == 1) or (curPNum == 2 and board.game_state() == -1)):
                return (1, None)
        return (0, None)

    def minimax(self, depth, isMaximizing, board):
        curPNum = 0
        if(isMaximizing):
            curPNum = self.pNum
        else:
            curPNum = self.pNum%2+1

        openPositions = board.open_positions()
        autoTie = board.is_auto_tie()
        checkWin = board.check_win()
        if(depth == 0 or checkWin or len(openPositions) == 0):
            return self.value(isMaximizing, board)

        if(isMaximizing == True): # maximizing player
            maxPos = openPositions[0]
            maxVal = -999 # negative infinity
            for pos in openPositions:
                tempBoard = deepcopy(board)
                tempBoard.update(curPNum, pos)
                curNode = self.minimax(depth-1, False, tempBoard)
                curVal = curNode[0]
                if(curVal > maxVal):
                    maxVal = curVal
                    maxPos = pos
            return (maxVal, maxPos)
        else: # minimizing player
            minPos = openPositions[0]
            minVal = 999 # positive infinity
            for pos in openPositions:
                tempBoard = deepcopy(board)
                tempBoard.update(curPNum, pos)
                curNode = self.minimax(depth-1, True, tempBoard)
                curVal = curNode[0]
                if(curVal < minVal):
                    minVal = curVal
                    minPos = pos
            return (minVal, minPos)

    def get_position(self, board, curRound):
        depth = board.dim**2 - curRound +1
        bestValue, bestPos = self.minimax(depth, True, board)
        return bestPos

class AlphaBetaMiniMaxAgent(Player):

    '''
    Purpose: An agent that employs an improvement to the above agent by applying alpha beta pruning.
    '''

    def __str__(self):
        return "Alpha Beta MiniMax Agent"

    def value(self, isMaximizing, board):
        if(isMaximizing):
            curPNum = self.pNum
        else:
            curPNum = self.pNum%2+1

        if(isMaximizing):
            if((curPNum == 1 and board.game_state() == -1) or (curPNum == 2 and board.game_state() == 1)):
                return (-1, None)
        if(not isMaximizing):
            if((curPNum == 1 and board.game_state() == 1) or (curPNum == 2 and board.game_state() == -1)):
                return (1, None)
        return (0, None)

    def minimax(self, depth, isMaximizing, board, alpha, beta):
        curPNum = 0
        if(isMaximizing):
            curPNum = self.pNum
        else:
            curPNum = self.pNum%2+1

        openPositions = board.open_positions()
        autoTie = board.is_auto_tie()
        checkWin = board.check_win()
        if(depth == 0 or checkWin or len(openPositions) == 0):
            return self.value(isMaximizing, board)

        if(isMaximizing == True): # maximizing player
            maxPos = openPositions[0]
            maxVal = -999
            for pos in openPositions:
                tempBoard = deepcopy(board)
                tempBoard.update(curPNum, pos)
                curNode = self.minimax(depth-1, False, tempBoard, alpha, beta)
                curVal = curNode[0]
                if(curVal > maxVal):
                    maxVal = curVal
                    maxPos = pos
                alpha = max(alpha, maxVal)
                if beta <= alpha:
                    break
            return (maxVal, maxPos)
        else: # minimizing player
            minPos = openPositions[0]
            minVal = 999
            for pos in openPositions:
                tempBoard = deepcopy(board)
                tempBoard.update(curPNum, pos)
                curNode = self.minimax(depth-1, True, tempBoard, alpha, beta)
                curVal = curNode[0]
                if(curVal < minVal):
                    minVal = curVal
                    minPos = pos
                beta = min(beta, minVal)
                if(beta <= alpha):
                    break
            return (minVal, minPos)

    def get_position(self, board, curRound):
        alpha, beta = -999, 999
        depth = board.dim**2 - curRound +1
        bestValue, bestPos = self.minimax(depth, True, board, alpha, beta)
        return bestPos
