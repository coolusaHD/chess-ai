import random
import time
import copy

class Agent:
    def __init__(self):
        self.move_queue = None
        self.color = 'black'
        self.nextMove = None
        self.counter = None
        self.currentDepth = None
        self.start = None
        self.timeout = None
        self.globalBestMove = None
        self.globalBestScore = None
        self.nextMoveScore = None

    def get_move(self):
        move = None
        while not self.move_queue.empty():
            move = self.move_queue.get()
        return move

    def update_move(self, move, score, depth):
        """
        :param move: Object of class Move, like a list element of gamestate.getValidMoves()
        :param score: Integer; not really necessary, just for informative printing
        :param depth: Integer; not really necessary, just for informative printing
        :return:
        """
        self.move_queue.put([move, score, depth])

    def clear_queue(self, outer_queue):
        self.move_queue = outer_queue

    def findBestMove(self, gs):
        """
        Helper method to make first recursive call

        Parameters
        ----------
        gs : Gamestate
            current state of the game
        validMoves : list
            list of valid moves
        returnQueue : Queue
            multithreading queue

        Returns
        -------
        Move

        """

        #get all valid moves
        startValidMoves = gs.getValidMoves()


        #alpha beta pruning to find best move
        self.globalBestMove = None
        self.globalBestScore = None
        self.nextMoveScore = None
        self.currentDepth = 2
        self.start = time.time()
        self.timeout = self.start + 19

        self.alphaBetaMax(gs, startValidMoves, self.currentDepth, -1000000, 1000000)
        
        #return best move as update_move
        self.update_move(self.globalBestMove, self.globalBestScore, self.currentDepth)
        

    def alphaBetaMax(self, gs, validMoves, depthLeft, alpha, beta):
        """
        Recursive method to find best move

        Parameters
        ----------
        gs : Gamestate
            current state of the game
        validMoves : list
            list of valid moves
        depthLeft : int
            depth of the current recursion
        alpha : int
            alpha value
        beta : int
            beta value

        Returns
        -------
        int

        """

        #check if time is up
        if time.time() > self.timeout:
            return -1000000

        #check if depth is reached
        if depthLeft == 0:
            print('GSmax:')
            print(gs)
            print('Evaluation max: ', self.evaluate(gs,True))
            return self.evaluate(gs,True)


        #check if there are more than one valid moves
        for move in validMoves:
            #get new gamestate
            newGamestate = copy.deepcopy(gs)
            #print(newGamestate)
            newGamestate.makeMove(move)

            #get new valid moves
            newValidMoves = newGamestate.getValidMoves()

            #check if new gamestate is not a terminal state
            self.nextMoveScore = self.alphaBetaMin(newGamestate, newValidMoves, depthLeft-1, alpha, beta)
            if self.nextMoveScore >= beta:
                return beta
            if self.nextMoveScore > alpha:
                alpha = self.nextMoveScore
                self.globalBestMove = move
                self.globalBestScore = alpha
            

        return alpha


    def alphaBetaMin(self, gs, validMoves, depthLeft, alpha, beta):
        """
        Recursive method to find best move

        Parameters
        ----------
        gs : Gamestate
            current state of the game
        depthLeft : int
            depth of the current recursion
        alpha : int
            alpha value
        beta : int
            beta value

        Returns
        -------
        int

        """

        #check if time is up
        if time.time() > self.timeout:
            return -1000000

        #check if depth is reached
        if depthLeft == 0:
            print('GSmin: ') 
            print(gs)
            print('Evaluation min: ', self.evaluate(gs,False))
            return self.evaluate(gs,False)


        #check if there are more than one valid moves
        for move in validMoves:
            #get new gamestate
            newGamestate = copy.deepcopy(gs)
            #print(newGamestate)
            newGamestate.makeMove(move)
            
            #get new valid moves
            newValidMoves = newGamestate.getValidMoves()

            #check if new gamestate is not a terminal state
            self.nextMoveScore = self.alphaBetaMax(newGamestate, newValidMoves, depthLeft-1, alpha, beta)
            if self.nextMoveScore <= alpha:
                return alpha
            if self.nextMoveScore < beta:
                beta = self.nextMoveScore
            

        return beta

    def reverseArray(array):
        """
        Helper method to reverse an array

        Parameters
        ----------
        array : list
            list to be reversed

        Returns
        -------
        list

        """
        return array[::-1]


    #total evaluation values per piece
    pawnSingleEval = 10
    rookSingleEval = 50
    knightSingleEval = 30
    bishopSingleEval = 30
    kingSingleEval = 1000


    #Evaluation array for white pieces
    pawnEvalWhite = [
        0.0,  0.0,  0.0,  0.0,  0.0,  0.0,
        5.0,  5.0,  5.0,  5.0,  5.0,  5.0,
        1.0,  2.0,  2.5,  2.5,  2.0,  1.0,
        0.5,  -0.5,  0.0,  0.5, -0.5, 0.0,
        0.5,  0.0,  -2.0,  2.0,  2.0,  0.0,
        0.0, 0.0, 0.0,  0.0,  0.0, 0.0,
    ]

    rookEvalWhite = [
        0.0,  0.0,  0.0,  0.0,  0.0,  0.0,
        5.0,  5.0,  5.0,  5.0,  5.0,  5.0,
        1.0,  1.0,  2.0,  3.0,  3.0,  2.0,
        0.5,  0.5,  1.0,  2.5,  2.5,  1.0,
        0.0,  0.0,  0.0,  2.0,  2.0,  0.0,
        0.5, -0.5, -.0,  0.0,  0.0, -1.0,
    ]

    knightEvalWhite = [
        -5.0, -4.0, -3.0, -3.0, -3.0, -4.0,
        -4.0, -2.0,  0.0,  0.0,  0.0, -2.0,
        -3.0,  0.0,  1.0,  1.5,  1.5,  0.0,
        -3.0,  0.5,  1.5,  2.0,  2.0,  0.5,
        -3.0,  0.0,  1.5,  2.0,  2.0,  0.0,
        -4.0, -2.0,  0.0,  0.0,  0.0, -2.0,
    ]

    bishopEvalWhite = [
      -2.0, -1.0, -1.0, -1.0, -1.0, -1.0,
        -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,
        -1.0,  0.0,  0.5,  1.0,  1.0,  0.0,
        -1.0,  0.5,  0.5,  1.0,  1.0,  0.5,
        -1.0,  0.0,  1.0,  1.0,  1.0,  0.0,
        -1.0,  0.5,  1.0,  1.0,  1.0,  0.5,
        -2.0, -1.0, -1.0, -1.0, -1.0, -1.0,
    ]


    kingEvalWhite = [
        -3.0, -4.0, -4.0, -5.0, -5.0, -4.0,
        -3.0, -4.0, -4.0, -5.0, -5.0, -4.0,
        -3.0, -4.0, -4.0, -5.0, -5.0, -4.0,
        -3.0, -4.0, -4.0, -5.0, -5.0, -4.0,
        -2.0, -3.0, -3.0, -4.0, -4.0, -3.0,
        -1.0, -2.0, -2.0, -2.0, -2.0, -2.0,
    ]

    #Evaluation array for black pieces
    pawnEvalBlack = reverseArray(pawnEvalWhite)
    rookEvalBlack = reverseArray(rookEvalWhite)
    knightEvalBlack = reverseArray(knightEvalWhite)
    bishopEvalBlack = reverseArray(bishopEvalWhite)
    kingEvalBlack = reverseArray(kingEvalWhite)

    def evaluate(self, gs, isMax):
        """
        Evaluate the gamestate

        Parameters
        ----------
        gs : GameState
            gamestate to be evaluated
        isMax : bool
            True if it is the max player's turn, False if it is the min player's turn

        Returns
        -------
        float

        """
        if self.color == 'white':
            if isMax:
                return self.evaluateWhite(gs)
            else:
                return self.evaluateBlack(gs)
        else:
            if isMax:
                return self.evaluateWhite(gs)
            else:
                return self.evaluateBlack(gs)
    

    def evaluateBlack(self, gs):
        """
        Evaluate the gamestate for black

        Parameters
        ----------
        gs : GameState
            gamestate to be evaluated

        Returns
        -------
        float

        """
        score = 0
        for i in range(0, 35):
            if self.getBoardFigure(gs, i) == 'bp':
                score += self.pawnSingleEval + self.pawnEvalBlack[i]
            if self.getBoardFigure(gs, i) == 'bN':
                score += self.knightSingleEval + self.knightEvalBlack[i]
            if self.getBoardFigure(gs, i) == 'bB':
                score += self.bishopSingleEval + self.bishopEvalBlack[i]
            if self.getBoardFigure(gs, i) == 'bR':
                score += self.rookSingleEval + self.rookEvalBlack[i]
            if self.getBoardFigure(gs, i) == 'bK':
                score += self.kingSingleEval + self.kingEvalBlack[i]
        return score

    def getBoardFigure(self,gs, i):
        """
        Get the figure at the given position

        Parameters
        ----------
        gs : GameState
            gamestate to access board
        i : int
            index


        Returns
        -------
        str

        """

        return gs.board[i]


    def evaluateWhite(self, gs):
        """
        Evaluate the gamestate for white

        Parameters
        ----------
        gs : GameState
            gamestate to be evaluated

        Returns
        -------
        float

        """
        score = 0
        for i in range(0, 35):
            if self.getBoardFigure(gs, i) == 'wp':
                score += self.pawnSingleEval + self.pawnEvalWhite[i]
            if self.getBoardFigure(gs, i) == 'wN':
                score += self.knightSingleEval + self.knightEvalWhite[i]
            if self.getBoardFigure(gs, i) == 'wB':
                score += self.bishopSingleEval + self.bishopEvalWhite[i]
            if self.getBoardFigure(gs, i) == 'wR':
                score += self.rookSingleEval + self.rookEvalWhite[i]
            if self.getBoardFigure(gs, i) == 'wK':
                score += self.kingSingleEval + self.kingEvalWhite[i]
        return score


    


            
        

        
    
        

        

        