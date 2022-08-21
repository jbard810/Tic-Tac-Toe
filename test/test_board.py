import pytest, sys, os, random
sys.path.append(os.path.abspath(os.path.join("..", "src")))
from Board import *

def test_tokens():
    '''
    Purpose: Tests the token string representation. Primarily serves to detect if someone changes the presentation of the game
    Test Cases:
        1. Empty Token (expected to have a string representation of " ")
        2. Cross Token (expected to have a string representation of "x")
        3. Nought Token (expected to have a string representation of "o")
    '''

    emptyTok, emptyTokStr = Token.EMPTY, " "
    crossTok, crossTokStr = Token.CROSS, "x"
    noughtTok, noughtTokStr = Token.NOUGHT, "o"

    assert str(emptyTok) == emptyTokStr # Test Case 1
    assert str(crossTok) == crossTokStr # Test Case 2
    assert str(noughtTok) == noughtTokStr # Test Case 3

def test_board_init():
    '''
    Purpose: Tests the initialization of the game board.
    Test Cases (ran on board dimensions ranging from 3 to 10):
        1. Tests that the board is initialized to empty tokens
        2. Tests that the proper number of positions are in the board (expected to be n^2 for a board of dimension n)
    '''

    all_tokens_none = True # flag for ensuring tokens are initialized to Token.EMPTY

    for n in range(3,11):
        b = Board(dim = n)
        numPositions = 0
        for i in range(b.dim):
            for j in range(b.dim):
                if(b.board[i][j] != Token.EMPTY):
                    all_tokens_none = False
                numPositions += 1
        assert all_tokens_none == True # Test Case 1
        assert numPositions == n**2 # Test Case 2

def test_is_full():
    '''
    Purpose: Tests the functionality of the is_full() function of the Board class.
    Test Cases (ran on board dimensions ranging from 3 to 10):
        1. Empty board (expected to return False)
        2. Non-full board with a random number of Tokens (expected to return False)
        3. Board with all positions filled (expected to return an empty list)
    '''
    for n in range(3,11):
        # ---------- Test Case 1 ----------
        b1 = Board(dim = n)
        assert b1.is_full() == False

        # ---------- Test Case 2 ----------
        b2 = Board(dim = n)
        numPostions = random.randint(1, n**2-1)
        positions = random.sample(b2.open_positions(), numPostions)
        pNum = 1
        for pos in positions:
            if(pNum == 1):
                b2.update(1, pos)
                pNum = 2
            else:
                b2.update(2, pos)
                pNum = 1
        assert b2.is_full() == False

        # ---------- Test Case 3 ----------
        b3 = Board(dim = n)
        positions = [(i, j) for i in range(b3.dim) for j in range(b3.dim)]
        pNum = 1
        for pos in positions:
            row, col = pos[0], pos[1]
            if(pNum == 1):
                b3.update(1, pos)
                pNum == 2
            else:
                b3.update(2, pos)
                pNum == 1
        assert b3.is_full() == True

def test_board_open_positions():
    '''
    Purpose: Tests the functionality of the open_positions() function of the Board class.
    Test Cases (ran on board dimensions ranging from 3 to 10):
        1. Empty board (expected to return a list of all posible positions [(0, 0), ..., (self.dim-1, self.dim-1)]
        2. Non-full board with a random number of Tokens (expected to return False) (expected to return a list that excludes all of the positions played)
        3. Board with all positions filled (expected to return an empty list)
    '''
    for n in range(3,11):
        # ---------- Test Case 1 ----------
        b1 = Board(dim = n)
        positions = [(i,j) for i in range(b1.dim) for j in range(b1.dim)]
        assert b1.open_positions() == positions

        # ---------- Test Case 2 ----------
        b2 = Board(dim = n)
        numPostions = random.randint(1, n**2-1)
        positions = random.sample(b2.open_positions(), numPostions)
        pNum = 1
        for pos in positions:
            if(pNum == 1):
                b2.update(1, pos)
                pNum = 2
            else:
                b2.update(2, pos)
                pNum = 1
            assert pos not in b2.open_positions()

        # ---------- Test Case 3 ----------
        b3 = Board(dim = n)
        positions = [(i, j) for i in range(b3.dim) for j in range(b3.dim)]
        pNum = 1
        for pos in positions:
            row, col = pos[0], pos[1]
            if(pNum == 1):
                b3.update(1, pos)
                pNum == 2
            else:
                b3.update(2, pos)
                pNum == 1
        assert b3.open_positions() == []


def test_board_update():
    '''
    Purpose: Tests the functionality of update() in the Board class.
    Test Cases (ran on board dimensions ranging from 3 to 10):
        1. Tests if the tokens are properly placed according the player number and position
        2. Tries to place a token on top of every position that is played in test case 1 (expected to return an exception)
            a) Places the token as the same player
            b) Places the token as the other player
    '''
    for n in range(3,11):
        b = Board(dim = n)
        numPositions = random.randint(1, n**2)
        positions = random.sample(b.open_positions(), numPositions)
        pNum = 1
        for pos in positions:
            row, col = pos[0], pos[1]
            if(pNum == 1):
                b.update(pNum, pos)
                assert b.board[row][col] == Token.CROSS # Test Case 1
                with pytest.raises(Exception):
                    b.update(1, pos) # Test Case 2a
                    b.update(2, pos) # Test Case 2b
                pNum = 2
            else:
                b.update(pNum, pos)
                assert b.board[row][col] == Token.NOUGHT
                with pytest.raises(Exception):
                    b.update(2, pos) # Test Case 2a
                    b.update(1, pos) # Test Case 2b
                pNum = 1


def test_board_clear():
    '''
    Purpose: Tests the functionality of the clear() function of the Board class.
    Test Cases (ran on board dimensions ranging from 3 to 10):
        1. Empty board
        2. Non-full board with a random number of Tokens
        3. Board with all positions filled
    '''
    for n in range(3,11):
        emptyBoard = Board(dim = n)
        # ---------- Test Case 1 ----------
        b1 = Board(dim = n)
        b1.clear()
        assert b1 == emptyBoard

        # ---------- Test Case 2 ----------
        b2 = Board(dim = n)
        numPostions = random.randint(1, n**2-1)
        positions = random.sample(b2.open_positions(), numPostions)
        pNum = 1
        for pos in positions:
            if(pNum == 1):
                b2.update(1, pos)
                pNum = 2
            else:
                b2.update(2, pos)
                pNum = 1
        b2.clear()
        assert b2 == emptyBoard

        # ---------- Test Case 3 ----------
        b3 = Board(dim = n)
        positions = [(i, j) for i in range(b3.dim) for j in range(b3.dim)]
        pNum = 1
        for pos in positions:
            row, col = pos[0], pos[1]
            if(pNum == 1):
                b3.update(1, pos)
                pNum == 2
            else:
                b3.update(2, pos)
                pNum == 1
        b3.clear()
        assert b3 == emptyBoard


def test_board_game_state():
    '''
    Purpose: Tests the functionality of game_state() in the Board class.
    Test Cases (ran on board dimensions ranging from 3 to 10):
        1. Tests for ties on the empty board (expected to return 0)
        2. Tests for major diagonal wins
            a) Ties while the diagonals are being filled in (expected to return 0)
            b) Player 1 winning (expected to return 1)
            c) Player 2 Winning (expected to return -1)
        3. Tests for minor diagonal wins
            a) Ties while the minor diagonals are being filled in (expected to return 0)
            b) Player 1 winning (expected to return 1)
            c) Player 2 Winning (expected to return -1)
        4. Test for wins along the rows
            a) Ties while the rows are being filled in (expected to return 0)
            b) Player 1 winning (expected to return 1)
            c) Player 2 Winning (expected to return -1)
        5. Tests for wins along the columns
            a) Ties while the columns are being filled in (expected to return 0)
            b) Player 1 winning (expected to return 1)
            c) Player 2 Winning (expected to return -1)
    '''
    for n in range(3,11):
        # ---------- Test Case 1 ----------
        b1 = Board(dim = n)
        assert b1.game_state() == 0

        # ---------- Test Case 2 ---------
        b2p1 = Board(dim = n)
        b2p2 = Board(dim = n)
        winningPositions = [(i,i) for i in range(b2p1.dim)]
        partACount = 1
        for pos in winningPositions:
            if(partACount < len(winningPositions)):
                assert b2p1.game_state() == 0 # Test Case 2a
                assert b2p2.game_state() == 0 # Test Case 2a
            b2p1.update(1, pos)
            b2p2.update(2, pos)
            partACount += 1
        assert b2p1.game_state() == 1 # Test Case 2b
        assert b2p2.game_state() == -1 # Test Case 2c

        # ---------- Test Case 3 ---------
        b3p1 = Board(dim = n)
        b3p2 = Board(dim = n)
        winningPositions = [(i,b3p1.dim-(i+1)) for i in range(b3p1.dim)]
        partACount = 1
        for pos in winningPositions:
            if(partACount < len(winningPositions)):
                assert b3p1.game_state() == 0 # Test Case 3a
                assert b3p2.game_state() == 0 # Test Case 3a
            b3p1.update(1, pos)
            b3p2.update(2, pos)
            partACount += 1
        assert b3p1.game_state() == 1 # Test Case 3b
        assert b3p2.game_state() == -1 # Test Case 3c

        # ---------- Test Case 4 ---------
        b4p1 = Board(dim = n)
        b4p2 = Board(dim = n)
        for i in range(b4p1.dim):
            winningPositions = [(i,j) for j in range(b4p1.dim)]
            partACount = 1
            for pos in winningPositions:
                if(partACount < len(winningPositions)):
                    assert b4p1.game_state() == 0 # Test Case 4a
                    assert b4p2.game_state() == 0 # Test Case 4a
                b4p1.update(1, pos)
                b4p2.update(2, pos)
                partACount += 1
            assert b4p1.game_state() == 1 # Test Case 4b
            b4p1.clear()
            assert b4p2.game_state() == -1 # Test Case 4c
            b4p2.clear()

        # ---------- Test Case 5 ---------
        b5p1 = Board(dim = n)
        b5p2 = Board(dim = n)
        for i in range(b5p1.dim):
            winningPositions = [(j,i) for j in range(b5p1.dim)]
            partACount = 1
            for pos in winningPositions:
                if(partACount < len(winningPositions)):
                    assert b5p1.game_state() == 0 # Test Case 5a
                    assert b5p2.game_state() == 0 # Test Case 5a
                b5p1.update(1, pos)
                b5p2.update(2, pos)
                partACount += 1
            assert b5p1.game_state() == 1 # Test Case 5b
            b5p1.clear()
            assert b5p2.game_state() == -1 # Test Case 5c
            b5p2.clear()

def test_winning_positions():
    '''
    Purpose: Test the winning_positions() function of the board class
    '''
    b1 = Board()
    b1.update(1, (0,0))
    b1.update(2, (1,1))
    b1.update(1, (0,1))
    b1.update(2, (2,0))
    assert b1.winning_positions(2) == [(0,2)]

def test_losing_positions():
    '''
    Purpose: Test the losing_positions() function of the board class
    '''
    b1 = Board()
    b1.update(1, (0,0))
    b1.update(2, (1,1))
    b1.update(1, (0,1))
    b1.update(2, (2,0))
    assert b1.losing_positions(2) == [(0,2)]
