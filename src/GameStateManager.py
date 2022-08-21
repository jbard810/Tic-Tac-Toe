from Board import *
from Agent import *

class GameStateManager():

    '''
    Purpose: Class for managing the how the players interact with the environment at each round.
    '''

    def __init__(self, board = Board(), p1 = Player(pNum=1), p2 = Player(pNum=2)):
        self.board = board
        self.p1 = p1
        self.p2 = p2


    def run_game(self):
        '''
        Purpose: Function that serves as a user interface for playing in the console.
        '''
        checkWin = False
        curRound = 1
        noMovesLeft = False

        while((not checkWin) and (not noMovesLeft)):
            numPositions = len(self.board.open_positions())
            if(curRound%2 == 1 and numPositions != 0 and not checkWin):
                print("- - - - - - - - - - Player 1 - - - - - - - - - -")
                print("")
                print(self.board)
                pos = self.p1.get_position(self.board, curRound)
                self.board.update(1, pos)
                numPositions = len(self.board.open_positions())
                curCheckWin = self.board.check_win()
                if(curCheckWin):
                    checkWin = True
                if(numPositions == 0):
                    noMovesLeft = True
            if(curRound%2 == 0 and numPositions != 0 and not checkWin):
                print("- - - - - - - - - - Player 2 - - - - - - - - - -")
                print("")
                print(self.board)
                pos = self.p2.get_position(self.board, curRound)
                self.board.update(2, pos)
                numPositions = len(self.board.open_positions())
                curCheckWin = self.board.check_win()
                if(curCheckWin):
                    checkWin = True
                if(numPositions == 0):
                    noMovesLeft = True
            curRound+=1

        finalGameState = self.board.game_state()

        if(finalGameState == 1):
            print("Final Outcome: Player 1 Wins")
        elif(finalGameState == -1):
            print("Final Outcome: Player 2 Wins")
        else:
            print("Final Outcome: Both Players Tie")

    def run_trial(self):

        '''
        Purpose: Function that runs a given trial for the simulation class.
        '''

        curRound = 1
        checkWin = True
        checkTie = False
        gamePositionSummary = {}
        gameBoardSummary = {}
        openPositions = self.board.open_positions()

        while((checkWin) and (not checkTie)):

            if(curRound%2 == 1 and checkWin and (not checkTie)):
                pos = self.p1.get_position(self.board, curRound)
                gamePositionSummary[curRound] = pos
                self.board.update(1, pos)
                curCheckWin = self.board.check_win()
                curCheckTie = self.board.is_auto_tie()
                if(curCheckWin or (not curCheckTie)):
                    checkWin = False
                    checkTie = True

            if(curRound%2 == 0 and checkWin and (not checkTie)):
                pos = self.p2.get_position(self.board, curRound)
                gamePositionSummary[curRound] = pos
                self.board.update(2, pos)
                curCheckWin = self.board.check_win()
                curCheckTie = self.board.is_auto_tie()
                if(curCheckWin or (not curCheckTie)):
                    checkWin = False
                    checkTie = True

            curRound += 1

        finalGameState = self.board.game_state()

        return finalGameState, gamePositionSummary
