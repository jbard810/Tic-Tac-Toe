import pytest, sys, os, random
sys.path.append(os.path.abspath(os.path.join("..", "src")))
from Agent import *
from contextlib import contextmanager
from io import StringIO

# ---------- Console Player Agent Testing ----------

def test_simple_agent():
    agent1 = SimpleAgent(pNum = 1)
    agent2 = SimpleAgent(pNum = 2)

    # ---------- Test Case 1 ----------
    b1 = Board()
    b1.update(1, (0,0))
    b1.update(2, (1,1))
    b1.update(1, (0,1))
    b1.update(2, (2,0))
    assert agent1.get_position(b1, 5) == (0,2) # should attempt to block player 2 from winning
    assert agent2.get_position(b1, 5) == (0,2) # should attempt to block player 2 from winning


def test_minimax_agent():
    agent1 = MiniMaxAgent(pNum = 1)
    agent2 = MiniMaxAgent(pNum = 2)

    # ---------- Test Case 1 ----------
    b1 = Board()
    b1.update(1, (0,0))
    b1.update(2, (1,1))
    b1.update(1, (0,1))
    b1.update(2, (2,0))
    assert agent1.get_position(b1, 5) == (0,2) # should attempt to block player 2 from winning
    assert agent2.get_position(b1, 5) == (0,2) # should attempt to block player 2 from winning

    # ---------- Test Case 2 ----------
    b2 = Board()
    agent1 = MiniMaxAgent(pNum = 1)
    agent2 = MiniMaxAgent(pNum = 2)
    validFirstMovesP1 = [(0,0), (0,b2.dim-1), (b2.dim-1,0), (b2.dim-1,b2.dim-1)]
    assert agent1.get_position(b2, 1) in validFirstMovesP1


'''
@contextmanager
def replace_stdin(target):
    orig = sys.stdin
    sys.stdin = target
    yield
    sys.stdin = orig

def test_player_get_position():
    consoleAgent = Player()
    with replace_stdin(StringIO("(0,0)")):
        pos = consoleAgent.get_position()
        assert pos == (0,0)
    with replace_stdin(StringIO("(0,5)")):
        pos = consoleAgent.get_position()
        assert pos == (0,5)
    with replace_stdin(StringIO("(3,9)")):
        pos = consoleAgent.get_position()
        assert pos == (3,9)
'''
