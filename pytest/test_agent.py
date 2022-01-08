import pytest
from ChessEngine import GameState, Move
from student_agents.template import Agent
import copy
import time


    ##TESTING###

gs = GameState()
agent = Agent()




@pytest.mark.parametrize("gs", [gs])
def test_evaluation(gs):


    eval1 = agent.evaluateBoard(gs)

    move = gs.getValidMoves()[0]
    gs.makeMove(move)

    eval2 = agent.evaluateBoard(gs)

    gs.undoMove()

    eval3 = agent.evaluateBoard(gs)

    assert eval1 == eval3


@pytest.mark.parametrize("gs", [gs])
def test_hash(gs):

    agent.__init__()

    assert agent.zobristTable != {}

    hash1 = agent.hashBoard(gs)

    move = gs.getValidMoves()[0]
    gs.makeMove(move)

    hash2 = agent.hashBoard(gs)

    gs.undoMove()

    hash3 = agent.hashBoard(gs)

    assert hash1 == hash3


@pytest.mark.parametrize("gs1,gs2", [(gs,gs)])
def test_hashWithMultipeMoves(gs1, gs2):

    agent.__init__()


    hashStart1 = agent.hashBoard(gs1)
    hashStart2 = agent.hashBoard(gs2)

    assert hashStart1 == hashStart2, "Start Hashes are not equal"

    #print('start')

    #print(gs1.board)
    #print(gs2.board)


    move1 = Move((1,0), (2,0), gs1.board)
    move2 = Move((1,3), (5,3), gs1.board)


    gs1.makeMove(move1)
    gs1.makeMove(move2)

    gs2.makeMove(move2)
    gs2.makeMove(move1)

    #print('after')

    #print(gs1.board)
    #print(gs2.board)

    hash1 = agent.hashBoard(gs1)
    hash2 = agent.hashBoard(gs2)

    eval1 = agent.evaluateBoard(gs1)
    eval2 = agent.evaluateBoard(gs2)

    assert hash1 == hash2, "Hashes after move are not equal"

    assert gs1.board == gs2.board, "Boards are not equal"

    assert eval1 == eval2, "Evaluations are not equal"


def test_evaluateBoard():

    gs = GameState()

    gs.board = ['bR', 'bB', 'bN', 'bK', 'bB', 'bR',
                'bp', 'bp', 'bp', 'bp', 'bp', 'bp',
                '--', '--', '--', '--', '--', '--',
                '--', '--', '--', '--', '--', '--',
                'wp', 'wp', 'wp', 'wp', 'wp', 'wp',
                'wR', 'wB', 'wN', 'wK', 'wB', 'wR']

    gs.whiteToMove = True

    eval1 = agent.evaluateBoard(gs)
    gs.whiteToMove = False
    eval2 = agent.evaluateBoard(gs)

    assert (eval1 - eval2) == 0, "Evaluations are not equal"

    print(eval1)
    print('gegen')
    print(eval2)

    gs.board = ['bR', 'bB', 'bN', 'bK', 'bB', 'bR',
                'bp', 'bp', '--', 'bp', 'bp', 'bp',
                '--', '--', '--', '--', '--', '--',
                '--', '--', '--', '--', '--', '--',
                'wp', 'wp', 'wp', 'wp', 'wp', 'wp',
                'wR', 'wB', 'wN', 'wK', 'wB', 'wR']

    gs.whiteToMove = True

    eval3 = agent.evaluateBoard(gs)
    gs.whiteToMove = False
    eval4 = agent.evaluateBoard(gs)

    print(eval3)
    print('gegen')
    print(eval4)


def test_firstMove():

    gs = GameState()

    gs.board = ['bR', 'bB', '--', 'bK', 'bB', 'bR',
                'bp', 'bp', 'bp', 'bp', 'bp', 'bp',
                '--', 'wB', '--', '--', '--', '--',
                '--', '--', '--', 'wp', '--', '--',
                'wp', 'wp', 'wp', '--', 'wp', 'wp',
                'wR', 'wB', 'wN', 'wK', '--', 'wR']

    agent.color = 'black'
    eval1 = agent.evaluateBoard(gs)

    gs.board = ['bR', 'bB', '--', 'bK', 'bB', 'bR',
                'bp', 'bp', '--', 'bp', 'bp', 'bp',
                '--', 'bp', '--', '--', '--', '--',
                '--', '--', '--', 'wp', '--', '--',
                'wp', 'wp', 'wp', '--', 'wp', 'wp',
                'wR', 'wB', 'wN', 'wK', '--', 'wR']

    agent.color = 'black'
    eval2 = agent.evaluateBoard(gs)

    print(eval1)
    print('gegen')
    print(eval2)

    assert eval1 < eval2, "Evaluation for first move are wrong" 




def test_evaluationTime():

    count = 0
    gs = GameState()    
    
    gs.board = ['bR', 'bB', 'bN', 'bK', 'bB', 'bR',
                'bp', 'bp', 'bp', 'bp', 'bp', 'bp',
                '--', '--', '--', '--', '--', '--',
                '--', '--', '--', '--', '--', '--',
                'wp', 'wp', 'wp', 'wp', 'wp', 'wp',
                'wR', 'wB', 'wN', 'wK', 'wB', 'wR']

    gs.makeMove(gs.getValidMoves()[0])

    start = time.time() 
    while time.time() - start < 1:

        agent.evaluateBoard(gs)
        count +=1

    print(count)
    assert count > 7000, "Evaluation is too slow"


def test_hashingMove():

    agent.__init__()

    gs = GameState()

    gs.board = ['bR', 'bB', 'bN', 'bK', 'bB', 'bR',
                'bp', 'bp', 'bp', 'bp', 'bp', 'bp',
                '--', '--', '--', '--', '--', '--',
                '--', '--', '--', '--', '--', '--',
                'wp', 'wp', 'wp', 'wp', 'wp', 'wp',
                'wR', 'wB', 'wN', 'wK', 'wB', 'wR']

    hash1 = agent.hashBoard(gs)

    move = gs.getValidMoves()[0]

    agent.hashedBoard = agent.hashBoard(gs)

    agent.updatezTableFromMove(move)

    hash2 = agent.hashedBoard

    gs.board = ['bR', 'bB', 'bN', 'bK', 'bB', 'bR',
                'bp', 'bp', 'bp', 'bp', 'bp', 'bp',
                '--', '--', '--', '--', '--', '--',
                '--', '--', '--', '--', '--', '--',
                'wp', 'wp', 'wp', 'wp', 'wp', 'wp',
                'wR', 'wB', 'wN', 'wK', 'wB', 'wR']

    gs.makeMove(move)

    hash3 = agent.hashBoard(gs)

    assert hash2 == hash3, "Hashes after move are not equal"



def test_indexToPosition():
    
    index = 0
    position = agent.indexToPosition(index)

    assert position == (0,0), "Index to position is wrong"

    index = 36
    position = agent.indexToPosition(index)

    assert position == (5,5), "Index to position is wrong"

















