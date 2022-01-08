import random
import time
import copy
import datetime

alhpa_cutoff_counter = 0
beta_cutoff_counter = 0

class Agent:
    def __init__(self):
        self.move_queue = None
        self.color = None
        self.nextMove = None
        self.counter = None
        self.currentDepth = None
        self.start = None
        self.timeout = None
        self.globalBestMove = None
        self.globalBestScore = None
        self.nextMoveScore = None


        self.alpha_cutoff_counter = 0
        self.beta_cutoff_counter = 0
        self.tableCounter = 0

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
        None but updates the returnQueue

        """
        
        #get color of Agent
        if gs.whiteToMove:
            self.color = 'white'
        else:
            self.color = 'black'


        #alpha beta pruning to find best move
        
        self.nextMoveScore = None
        self.currentDepth = 0
        self.start = datetime.datetime.now()
        self.timeout = self.start + datetime.timedelta(seconds=18)


        #get all valid moves
        startValidMoves = gs.getValidMoves()
        #to prevent return None initializing with first move
        self.globalBestMove = startValidMoves[0]
        self.globalBestScore = -float('inf')


        #start iterative deepening 
        while datetime.datetime.now() < self.timeout:
            self.currentDepth += 1
            print('start on depth: ', self.currentDepth)
            

            for move in startValidMoves:
                
                #copy gamestate
                copyGS = copy.deepcopy(gs)

                #make move
                copyGS.makeMove(move)
                #print('look for move:' + str(move.moveID) + 'and' + str(self.currentDepth))
                #calculate score
                score = self.alphaBeta(copyGS, self.currentDepth, -float('inf'), float('inf'), True)

                if score != None and score != float('inf') and score > self.globalBestScore:
                    self.globalBestMove = move
                    self.globalBestScore = score
           
            print('Actual cutoffs: alpha %d, beta %d' % (self.alpha_cutoff_counter, self.beta_cutoff_counter))
            #print('Table counter: ', self.tableCounter)

        #return best move as update_move
        self.update_move(self.globalBestMove, self.globalBestScore, self.currentDepth)
            



    def alphaBeta(self, gs, depth, alpha, beta, maxPlayer):
        """
        Recursive method to find best move

        Parameters
        ----------
        gs : GameState
            gamestate to be evaluated
        depth : int
            depth of recursion
        alpha : float
            alpha value
        beta : float
            beta value
        maxPlayer : bool
            True if maxPlayer, False if minPlayer

        Returns
        -------
        float

        """
                    #check for timeout
        if datetime.datetime.now() > self.timeout:
            return None

        #check for endgame
        if depth == 0 or gs.checkMate or gs.staleMate or gs.threefold or gs.draw:
            return self.evaluateBoard(gs)
        

        #check for maxPlayer
        if maxPlayer:

            validMoves = gs.getValidMoves()

            for move in validMoves:

                #copy gamestate
                copyGS = copy.deepcopy(gs)

                #make move
                copyGS.makeMove(move)

                #recursive call
                score = self.alphaBeta(copyGS, depth - 1, alpha, beta, False)

                if score is None:
                    return alpha

                if score >= beta:
                    self.beta_cutoff_counter += 1
                    return beta

                if score > alpha:
                    alpha = score
            
            return alpha

        #check for minPlayer
        else:

            validMoves = gs.getValidMoves()

            for move in validMoves:

                #copy gamestate
                copyGS = copy.deepcopy(gs)

                #make move
                copyGS.makeMove(move)

                #recursive call
                score = self.alphaBeta(copyGS, depth - 1, alpha, beta, True)

                if score is None:
                    return beta

                if score <= alpha:
                    self.alpha_cutoff_counter += 1
                    return alpha

                if score < beta:
                    beta = score
            
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
    evaluationValuesOfPieces = {'p': 10, 'N': 40, 'B': 30, 'R': 50, 'K': 900}

    #Evaluation array for white pieces
    pawnEvalWhite = [
        0.0,  0.0,  0.0,  0.0,  0.0,  0.0,
        5.0,  5.0,  5.0,  5.0,  5.0,  5.0,
        1.5,  2.5,  3.5,  3.5,  2.5,  1.5,
        0.0,  0.0,  0.0,  0.0,  0.0,  0.0,
        0.5,  1.0, -2.0, -2.0,  1.0,  0.5,
        0.0,  0.0,  0.0,  0.0,  0.0,  0.0,
    ]

    rookEvalWhite = [
        0.0,  0.0,  0.0,  0.0,  0.0,  0.0,
       -0.5,  1.0,  1.0,  1.0,  1.0, -0.5,
       -0.5,  0.0,  0.0,  0.0,  0.0, -0.5,
       -0.5,  0.0,  0.0,  0.0,  0.0, -0.5,
       -0.5,  0.0,  0.0,  0.0,  0.0, -0.5,
        0.0,  0.0,  1.0,  1.0,  0.0,  0.0,
    ]

    knightEvalWhite = [
        -5.0, -2.0, -1.0, -1.0, -2.0, -5.0,
        -3.0, -2.0,  0.5,  0.5,  0.0, -3.0,
        -2.0,  1.0,  2.0,  2.0,  1.0,  0.0,
        -2.0,  1.0,  2.0,  2.0,  1.0,  0.5,
        -3.0,  0.0,  0.5,  0.5,  0.0, -3.0,
        -5.0, -2.0, -1.0, -1.0, -2.0, -5.0,
    ]

    bishopEvalWhite = [
        -2.0, -1.0, -1.0, -1.0, -1.0, -2.0,
        -1.0,  0.0,  0.0,  0.0,  0.0, -1.0,
        -1.0,  0.5,  0.0,  0.0,  0.5, -1.0,
        -1.0,  1.0,  1.0,  1.0,  1.0, -1.0,
        -1.0,  0.5,  0.0,  0.0,  0.5, -1.0,
        -2.0, -1.0, -1.0, -1.0, -1.0, -2.0,
    ]

    kingEvalWhite = [
        -4.0, -4.0, -5.0, -5.0, -4.0, -4.0,
        -3.0, -4.0, -5.0, -5.0, -5.0, -3.0,
        -2.5, -3.0, -4.0, -4.0, -3.0, -2.5,
        -1.5, -2.0, -2.0, -2.0, -2.0, -1.5,
         2.0,  2.0,  0.0,  0.0,  2.0,  2.0,
         2.0,  3.0,  1.0,  1.0,  3.0,  2.0,
    ]

    #Evaluation array for black pieces
    pawnEvalBlack = reverseArray(pawnEvalWhite)
    rookEvalBlack = reverseArray(rookEvalWhite)
    knightEvalBlack = reverseArray(knightEvalWhite)
    bishopEvalBlack = reverseArray(bishopEvalWhite)
    kingEvalBlack = reverseArray(kingEvalWhite)

    validationArrayOfPieces = {'wp': pawnEvalWhite, 'wN': knightEvalWhite, 'wB': bishopEvalWhite, 'wR': rookEvalWhite, 'wK': kingEvalWhite, 'bp': pawnEvalBlack, 'bN': knightEvalBlack, 'bB': bishopEvalBlack, 'bR': rookEvalBlack, 'bK': kingEvalBlack}

    checkEval = 100
    checkMateEval = 10000


    def evaluateBoard(self, gs):
        """
        Evaluate the gamestate for the board 
        score is the sum of the categories 

        Parameters
        ----------
        gs : GameState
            gamestate to be evaluated

        Returns
        -------
        float

        """
        score = 0
        
        #check for good checks for white
        #score += self.checkForGoodChecks(gs)

        #check material
        #print(gs)
        score += self.evalMaterial(gs)


        #check which color is to move
        #because after move gs.whiteToMove is switched
        if self.color == 'white':
            return score
        else:
            return -score


    def evalMaterial(self, gs):
        """
        Evaluate material on board

        Parameters
        ----------
        gs : GameState
            gamestate to be evaluated

        Returns
        -------
        int

        """
        score = 0

        for i in range(36):
            figure = gs.board[i]
            if figure[0] == 'b':
                factor = -1
            else:
                factor = 1

            if figure == '--':
                continue
            elif figure[1] == 'p':
                score += factor*(self.evaluationValuesOfPieces[figure[1]]+self.validationArrayOfPieces[figure][i])
            elif figure[1] == 'N':
                score += factor*(self.evaluationValuesOfPieces[figure[1]]+self.validationArrayOfPieces[figure][i])
            elif figure[1] == 'B':
                score += factor*(self.evaluationValuesOfPieces[figure[1]]+self.validationArrayOfPieces[figure][i])
            elif figure[1] == 'R':
                score += factor*(self.evaluationValuesOfPieces[figure[1]]+self.validationArrayOfPieces[figure][i])
            elif figure[1] == 'K':
                score += factor*(self.evaluationValuesOfPieces[figure[1]]+self.validationArrayOfPieces[figure][i])

        #return difference of material
        return score

    def checkForGoodChecks(self, gs):
        """
        Check for checks on board for current player

        Parameters
        ----------
        gs : GameState
            gamestate to be evaluated

        Returns
        -------
        int

        """

        score = 0

        if gs.inCheck:
            score -= self.checkEval
        if gs.checkMate:
            score -= self.checkmateEval

        return score










    


            
        

        
    
        

        

        