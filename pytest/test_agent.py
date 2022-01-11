import pytest
from ChessEngine import GameState, Move
from student_agents.template import Agent
import copy
import time


    ##TESTING###

gs = GameState()
agent = Agent()




def test_evaluation():

    gs = GameState()

    agent.__init__()

    eval1 = agent.evaluateBoard(gs)

    move = gs.getValidMoves()[0]
    gs.makeMove(move)

    eval2 = agent.evaluateBoard(gs)

    gs.undoMove()

    eval3 = agent.evaluateBoard(gs)

    assert eval1 == eval3


def test_hash():

    gs = GameState()

    agent.__init__()

    assert agent.zobristTable != {}

    hash1 = agent.hashBoard(gs)

    move = gs.getValidMoves()[0]
    gs.makeMove(move)

    hash2 = agent.hashBoard(gs)

    gs.undoMove()

    hash3 = agent.hashBoard(gs)

    assert hash1 == hash3



def test_evaluateBoard():

    gs = GameState()

    gs.board = ['bR', 'bB', 'bN', 'bK', 'bB', 'bR',
                'bp', 'bp', 'bp', 'bp', 'bp', 'bp',
                '--', '--', '--', '--', '--', '--',
                '--', '--', '--', '--', '--', '--',
                'wp', 'wp', 'wp', 'wp', 'wp', 'wp',
                'wR', 'wB', 'wN', 'wK', 'wB', 'wR']

    agent.color = 'white'

    eval1 = agent.evaluateBoard(gs)
    agent.color = 'black'
    eval2 = agent.evaluateBoard(gs)

    assert (eval1 + eval2) == 0, "Evaluations are not equal"

    #print(eval1)
    #print('gegen')
    #print(eval2)

    gs.board = ['bR', 'bB', 'bN', 'bK', 'bB', 'bR',
                'bp', 'bp', '--', 'bp', 'bp', 'bp',
                '--', '--', '--', '--', '--', '--',
                '--', '--', '--', '--', '--', '--',
                'wp', 'wp', 'wp', 'wp', 'wp', 'wp',
                'wR', 'wB', 'wN', 'wK', 'wB', 'wR']

    agent.color = 'white'

    eval3 = agent.evaluateBoard(gs)
    agent.color = 'black'
    eval4 = agent.evaluateBoard(gs)

    assert eval3 > eval4, "Evaluation are not greater"

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

    #print(eval1)
    #print('gegen')
    #print(eval2)

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

    #print(count)
    assert count > 5000, "Evaluation is too slow"


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

    hash2 = agent.updatezTableFromMove(hash1,move)

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

    """
        [C0    1     2     3     4     5   
    R0  '00', '01', '02', '03', '04', '05',
    1   '06', '07', '08', '09', '10', '11',
    2   '12', '13', '14', '15', '16', '17',
    3   '18', '19', '20', '21', '22', '23',
    4   '24', '25', '26', '27', '28', '29',
    5   '30', '31', '32', '33', '34', '35'
        ]
    """

    agent.__init__()

    
    index = 0
    position = agent.getPositionOfIndex(index)

    assert position == (0,0), "Index to position is wrong1"

    index = 25
    position = agent.getPositionOfIndex(index)

    #print(position)

    assert position == (4,1), "Index to position is wrong2"

    index = 16
    position = agent.getPositionOfIndex(index)

    #print(position)

    assert position == (2,4), "Index to position is wrong3"

    index = 35
    position = agent.getPositionOfIndex(index)

    assert position == (5,5), "Index to position is wrong4"


def test_king404():

    agent.__init__()

    gs = GameState()

    gs.board = [
                '--', 'bB', 'bK', '--', 'bB', 'wN',
                '--','bp', 'bp', '--', 'bp', 'bp',
                '--', '--', '--', '--', '--', '--',
                '--', 'wp', '--','--', '--', '--',
                'wB', '--', '--', '--','--', 'wp',
                'wR', '--', '--', '--', '--', '--']

    gs.whiteToMove = False

    agent.color = 'black'

    moves = gs.getValidMoves()

    #print(len(moves))

    assert moves != [], "King is in not found"

def test_evalCapture():

    agent.__init__()

    gs = GameState()

    gs.board = ['bR', 'bB', '--', 'bK', 'bB', 'bR',
                'bp', '--', 'bp', 'bp', 'bp', 'bp',
                '--', 'bp', '--', 'bN', '--', '--',
                '--', '--', '--', 'wp', 'wp', '--',
                'wp', 'wp', 'wp', '--', '--', 'wp',
                'wR', 'wB', 'wN', 'wK', 'wB', 'wR']

    gs.whiteToMove = True

    move = Move((3,4),(2,3),gs.board)

    gs.makeMove(move)
    

    eval = agent.evalCapture(move)
    print(eval)

    #assert eval == 11, "Eval capture is wrong1"
    assert eval > 0, "Eval capture is wrong2"


def test_defenseBehavior():

    agent.__init__()

    gs = GameState()

    gs.board = ['bR', 'bB', '--', 'bK', '--', 'bR',
                'bp', 'bp', 'bp', 'bp', 'bp', 'bp',
                '--', '--', '--', '--', '--', '--',
                '--', '--', '--', '--', '--', '--',
                'wp', 'wp', 'bB', 'wp', 'wp', 'wp',
                'wR', 'wB', 'wK', '--', 'wB', 'wR']

    gs.whiteToMove = True

    moves =gs.getValidMoves()

    for move in moves:
        print(move)
        gs.makeMove(move)
        print(gs)
        print('eval: ' + str(agent.evaluateBoard(gs)))
        gs.undoMove()


def test_evalPositionOfFigure():

    agent.__init__()

    gs = GameState()

    gs.board = ['bR', 'bB', '--', 'bK', '--', 'bR',
                'bp', 'bp', 'bp', 'bp', 'bp', 'bp',
                '--', '--', '--', '--', '--', '--',
                '--', '--', '--', '--', '--', '--',
                'wp', 'wp', 'bB', 'wp', 'wp', 'wp',
                'wR', 'wB', 'wK', '--', 'wB', 'wR']

    eval = agent.evalPositionOfFigure(gs,(3,4))


    



    














