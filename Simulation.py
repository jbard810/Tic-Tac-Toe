import sys, os
sys.path.append(os.path.abspath("src"))
from Board import *
from Agent import *
from GameStateManager import *

class Simulation():
    '''
    Purpose: Class that provides tools for simulating the way that two agents play over a sample of TicTacToe games.
    Attributes:
        - boardDim: integer value that specifies the dimensions of the board (default is 3)
        - agent1: is an agent object that will act as player 1 (default is the random agent)
        - agent2: is an agent object that will act as player 2 (default is the random agent)
        - sampleSize: integer value that specifies the number of samples that the simulation will go over (default is 1)
    Note: Possible agent choices can be found in the Agent.py file
    '''
    def __init__(self, boardDim = 3, agent1 = RandomAgent(1), agent2 = RandomAgent(2), sampleSize = 1):
        self.boardDim = boardDim
        self.agent1 = agent1
        self.agent2 = agent2
        self.sampleSize = sampleSize

    def run_simulation(self):
        '''
        Purpose: Function that runs the simulations and returns the data.
        '''
        simData = []
        num = 1
        for trialNum in range(self.sampleSize):
            print("Trial Number:", num)
            board = Board(self.boardDim)
            GSM = GameStateManager(board, self.agent1, self.agent2)
            trialOutcome, trialGamePositionSummary = GSM.run_trial()
            simData.append([trialOutcome, trialGamePositionSummary])
            num += 1
        return simData

    def trial_visualizer(self, trialData):
        '''
        Purpose: Allows one to visualize a particular round of from the simulation data from run_simulation().
        '''
        trialOutcome = trialData[0]
        trialGamePositionSummary = trialData[1]
        b = Board(self.boardDim)
        roundNum = 0
        for round in trialGamePositionSummary:
            roundNum += 1
            if(round%2==1):
                pos = trialGamePositionSummary[round]
                print("- - - - - - - - - - - Round", roundNum, " - - - - - - - - - - ")
                print("Position Placed: ", pos)
                b.update(1, pos)
                print(b)
            if(round%2==0):
                pos = trialGamePositionSummary[round]
                print("- - - - - - - - - - - Round", roundNum, " - - - - - - - - - - ")
                print("Position Placed: ", pos)
                b.update(2, pos)
                print(b)
        if(trialOutcome == 1):
            print("Trial Outcome: Player 1 Wins")
        elif(trialOutcome == -1):
            print("Trial Outcome: Player 2 Wins")
        else:
            print("Trial Outcome: Tie")

    def outcome_summary(self, simulationData):
        '''
        Purpose: Summarizes the number of times that the trial resulted in player 1 winning, player 2 winning, or both players coming to a tie.
        '''
        outcomeData = []
        for d in simulationData:
            outcomeData.append(d[0])
        numP1Wins = 0
        numP2Wins = 0
        numTies = 0
        numTrials = len(outcomeData)
        for outcome in outcomeData:
            if(outcome == 1):
                numP1Wins += 1
            elif(outcome == -1):
                numP2Wins += 1
            else:
                numTies += 1
        outcomeSummary = [numP1Wins, numP2Wins, numTies]
        return outcomeSummary

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
    # Example Usage of the tools provided by the Simulation class
    print("= = = = = = = = = Tic-tac-toe Simulation = = = = = = = = = \n")
    agent1 = AlphaBetaMiniMaxAgent(pNum = 1)
    agent2 = RandomAgent(pNum = 2)
    boardDim = 3
    sampleSize = 100
    sim = Simulation(boardDim, agent1, agent2, sampleSize)
    simData = sim.run_simulation()
    # Uncomment the following section if you wish to visualize the trials
    '''
    for trialData in simData:
        sim.trial_visualizer(trialData)
    '''
    outcomeSummary = sim.outcome_summary(simData)
    print("Number of Player 1 Wins: ", outcomeSummary[0])
    print("Number of Player 2 Wins: ", outcomeSummary[1])
    print("Number of Ties: ", outcomeSummary[2])
