from enum import Enum
from copy import deepcopy

class Token(Enum):
    '''
    Purpose: Class that defines enumerations for different game tokens.
    '''

    EMPTY = 0
    CROSS = 1
    NOUGHT = 2

    def __eq__(self, other):
        return self.value == other.value

    def __str__(self):
        strDict = {0: " ", 1: "x", 2: "o"}
        return strDict.get(self.value)

    def __repr__(self):
        strDict = {0: " ", 1: "x", 2: "o"}
        return strDict.get(self.value)

class Board():
    '''
    Purpose: Class that creates and manages the TicTacToe game board.
    Attributes:
        - self.dim: an integer value that represents how large the board will be
        - self.board: 2d list that stores the game tokens
    '''
    def __init__(self, dim = 3):
        self.dim = dim
        self.board = [self.dim*[Token.EMPTY] for i in range(self.dim)]

    def __str__(self):
        boardStr = ""
        hLines = "                   " + (3*self.dim + 1)*"-" + "                  " + "\n"
        for i in range(self.dim):
            bRow = self.board[i][0:self.dim]
            row = "                   " + " | ".join(str(tok) for tok in bRow) + "                   " + "\n"
            boardStr += row
            if(i < self.dim - 1):
                boardStr += hLines
        return boardStr

    def __repr__(self):
        boardStr = ""
        hLines = (3*self.dim + 1)*"-"+"\n"
        for i in range(self.dim):
            row = " | ".join(str(self.board[i][0:self.dim])) + "\n"
            boardStr += row
            if(i < self.dim - 1):
                boardStr += hLines
        return boardStr

    def __eq__(self, other):
        positions = [(i,j) for i in range(self.dim) for j in range(self.dim)]
        for pos in positions:
            row, col = pos[0], pos[1]
            if(self.board[row][col] != other.board[row][col]):
                return Fals
        return True

    def is_full(self):
        positions = [(i,j) for i in range(self.dim) for j in range(self.dim)]
        for pos in positions:
            row, col = pos[0], pos[1]
            if(self.board[row][col] == Token.EMPTY):
                return False
        return True

    def open_positions(self):
        '''
        Purpose: Function that returns all of the open positions.
        Output:
            - position: List of position tuples that the player can play in.
        '''
        positions = []

        if(self.is_full()):
            return positions
        else:
            for i in range(self.dim):
                for j in range(self.dim):
                    if(self.board[i][j] == Token.EMPTY):
                        positions.append((i,j))
            return positions

    def update(self, pNum: int, pos: tuple[int]):
        '''
        Purpose: Takes the player number and position they wish to play at, in order to update the current board state
        Inputs:
        - pNum: An integer value that represents the player position
            - 1 represents Player 1 (which means an "x" will be played)
            - 2 represents Player 2 (which means an "o" will be played)
        - pos: a integer tuple that represents a coordinate value
            - (0,0) represents the top left corner
            - (0, dim-1) represents the top right corner
            - (dim-1, 0) represents the bottom left corner
            - (dim-1, dim-1) represents the bottom right corner
        '''

        positions = self.open_positions()

        if(pos not in positions):
            msg = "This position is not open for play."
            raise Exception(msg)
        else:
            row, col = pos[0], pos[1]
            if(pNum == 1):
                self.board[row][col] = Token.CROSS
            if(pNum == 2):
                self.board[row][col] = Token.NOUGHT

    def clear(self):
        '''
        Purpose: Clears the entire board of non-empty tokens
        '''
        self.board = [self.dim*[Token.EMPTY] for i in range(self.dim) ]

    def game_state(self):
        '''
        Purpose: Checks the current game state of the board.
        Outputs:
            - gameState: value that represents the player that won
                -  0 is returned if there are no current winners
                -  1 is returned if Player 1 won the game
                - -1 is returned if Player 2 won the game
        '''
        # Initial Data for Detecting Diagonal Wins
        initMajDiagVal = self.board[0][0] # initial major diagonal value at the top right corner (0, 0)
        majDiagWin = True # flag for detecting a potential win along the major diagonal
        initMinDiagVal = self.board[0][self.dim-1] # initial minor diagonal value at the top left corner (0, self.dim-1)
        minDiagWin = True # flag for detecting a potential win along the minor diagonal

        # Nested loop that iterates through the board board
        for i in range(self.dim):

            # Initial Data for Detecting Row and Column Wins
            initHorVal = self.board[i][0] # initial horizontal value for the given row (i, 0)
            horWin = True # flag for detecting a potential win along the given row
            initVertVal = self.board[0][i] # initial horizontal value for the given column (0, i)
            vertWin = True # flag for detecting a potential win along the given column

            # Data for iterating diagonally
            curMajDiagVal = self.board[i][i] # The most current value for the major diagonal at the ith iteration that goes from (0, 0) to (self.dim-1, self.dim-1)
            curMinDiagVal = self.board[i][self.dim-(i+1)] # The most current value for the minor diagonal at the ith iteration that goes from (0, self.dim-1) to (self.dim-1, 0)

            # Diagonal Flag Logic
            if((majDiagWin == True) and ((curMajDiagVal == Token.EMPTY) or (curMajDiagVal != initMajDiagVal))):
                majDiagWin = False
            if((minDiagWin == True) and ((curMinDiagVal == Token.EMPTY) or (curMinDiagVal != initMinDiagVal))):
                minDiagWin = False

            # Return Statement Logic for Diagonal Wins
            if((i == (self.dim-1)) and (majDiagWin == True)):
                if(curMajDiagVal == Token.CROSS):
                    gameState = 1 # Player 1 Wins
                    return gameState
                else:
                    gameState = -1 # Player 2 Wins
                    return gameState
            if((i == (self.dim-1)) and (minDiagWin == True)):
                if(curMinDiagVal == Token.CROSS):
                    gameState = 1 # Player 1 Wins
                    return gameState
                else:
                    gameState = -1 # Player 2 Wins
                    return gameState

            for j in range(self.dim):

                # Data for iterating through the rows and colums
                curHorVal = self.board[i][j] # The most current value for the given horizontal row i as j varies through the columns
                curVertVal = self.board[j][i] # The most current value for the given vertical column i as j varies through the rows

                # Flag Logic for Horizontal and Vertical Wins
                if((horWin == True) and ((curHorVal == Token.EMPTY) or (curHorVal != initHorVal))):
                    horWin = False
                if((vertWin == True) and ((curVertVal == Token.EMPTY) or (curVertVal != initVertVal))):
                    vertWin = False

                # Return statement logic for horizontal and diagonal wins
                if((j == (self.dim-1)) and (horWin == True)):
                    if(curHorVal == Token.CROSS):
                        gameState = 1 # Player 1 Wins
                        return gameState
                    else:
                        gameState = -1 # Player 2 Wins
                        return gameState
                if((j == (self.dim-1)) and (vertWin == True)):
                    if(curVertVal == Token.CROSS):
                        gameState = 1 # Player 1 Wins
                        return gameState
                    else:
                        gameState = -1 # Player 2 Wins
                        return gameState
        gameState = 0 # Tie
        return gameState

    def check_win(self):
        return (self.game_state() == 1) or (self.game_state() == -1)

    def winning_positions(self, pNum):
        '''
        Purpose: Determines the positions the agent can place their token and win.
        '''
        positions = self.open_positions()
        winningPositions = []
        for pos in positions:
            tempBoard = deepcopy(self)
            tempBoard.update(pNum, pos)
            if(pNum == 1 and tempBoard.game_state() == 1):
                winningPositions.append(pos)
            if(pNum == 2 and tempBoard.game_state() == -1):
                winningPositions.append(pos)
        return winningPositions

    def losing_positions(self, pNum):
        '''
        Purpose: Determines the positions the opponent can place their token and win.
        '''
        positions = self.open_positions()
        losingPositions = []
        for pos in positions:
            tempBoard = deepcopy(self)
            tempBoard.update(pNum%2+1, pos)
            if(pNum == 1 and tempBoard.game_state() == -1):
                losingPositions.append(pos)
            if(pNum == 2 and tempBoard.game_state() == 1):
                losingPositions.append(pos)
        return losingPositions

    def is_auto_tie(self):
        '''
        Purpose: Determines if a tie is inevitable before the board is full.
        '''
        remainingRows = self.dim*[1]
        remainingColumns = self.dim*[1]
        remainingDiagonals = 2*[1]

        # Row and Column Checking
        for i in range(self.dim):
            curRow = []
            curCol = []
            for j in range(self.dim):
                curRow.append(self.board[i][j])
                curCol.append(self.board[j][i])
            if((Token.CROSS in curRow) and (Token.NOUGHT in curRow)):
                remainingRows[i] = 0
            if((Token.CROSS in curCol) and (Token.NOUGHT in curCol)):
                remainingColumns[i] = 0

        # Diagonal Checking
        majDiag = [self.board[i][i] for i in range(self.dim)]
        if((Token.CROSS in majDiag) and (Token.NOUGHT in majDiag)):
            remainingDiagonals[0] = 0
        minDiag = [self.board[i][self.dim-(i+1)] for i in range(self.dim)]
        if((Token.CROSS in minDiag) and (Token.NOUGHT in minDiag)):
            remainingDiagonals[1] = 0

        if((1 in remainingRows) or (1 in remainingColumns) or (1 in remainingDiagonals)):
            return False
        else:
            return True
