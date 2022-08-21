import sys, os
sys.path.append(os.path.abspath("src"))
from Board import *
from Agent import *
from GameStateManager import *

def play_again():
    playAgain = str(input("Would you like to play again? [Y,N]: "))
    if(playAgain == "Y"):
        return True
    elif(playAgain == "N"):
        return False
    else:
        print("The console did not understand your input. Please try again.")
        return play_again()


if __name__ == "__main__":
    '''
    Agent Options:
    - Player(): Agent for taking input from the console (could change both p1 and p2 to be Player() objects)
    - RandomAgent(): Agent that plays randomly
    - SimpleAgent(): Agent that implements a very simple heuristic by looking to see if it could currently win or is about to lose
    - MiniMaxAgent(): Agent that implements the minimax algorithm w/o alpha beta pruning (very slow and should probably avoid)
    - AlphaBetaMiniMaxAgent(): Agent that implements the minimax algorithm with alpha beta pruning (should use over the other implementation)
    Note: ALL agents require for you to specify a pNum attribute (1 is for p1 and 2 is for p2)
    '''
    # Editable Parameters
    p1 = Player(pNum = 1)
    p2 = AlphaBetaMiniMaxAgent(pNum = 2)
    print("= = = = = = = = = = Tic-tac-toe = = = = = = = =\n")
    print("Notes: ")
    print("- Player 1:", p1)
    print("- Player 2:", p2)
    print("- (0,0): is the top left corner")
    print("- (2,2): is the bottom right corner\n")

    gameNum = 1
    cont = True
    while(cont):
        print("= = = = = = = = = = = Game", gameNum,"= = = = = = = = = =\n")
        board = Board()
        gsm = GameStateManager(board, p1, p2)
        gsm.run_game()
        playAgain = play_again()
        if(playAgain):
            cont = True
            gameNum += 1
        else:
            cont = False
