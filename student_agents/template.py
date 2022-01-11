import random
import datetime
import copy

class Agent:
    def __init__(self):

        self.move_queue = None
        self.nextMove = None
        self.counter = None
        self.currentDepth = None
        self.start = None
        self.timeout = None
        self.globalBestMove = None
        self.globalBestScore = None
        self.nextMoveScore = None
        self.depth = None

        self.color = None
        self.alphaCutOffCounter = 0
        self.betaCutOffCounter = 0

        #---------Evaluation Values---------

        #ending game values
        self.checkEval = 20
        self.checkMateEval = 10000

        #Evaluation array for white pieces old
        self.pawnEvalWhite2 = [
            0 , 0 , 0 , 0 , 0 , 0 ,
            50, 50, 50, 50, 50, 50,
            20, 20, 30, 30, 20, 20,
            15, 0 , 20, 20, 10, 5 ,
            5 , 10,-20,-20, 10, 5 ,
            0 , 0 , 0 , 0 , 0 , 0  
        ]

        self.rookEvalWhite2 = [
            0 , 0 , 0 , 0 , 0 , 0 ,
            5 ,10 ,10 ,10 ,10 , 5 ,
            0 , 0 , 0 , 0 , 0 , 0 ,
            0 , 0 , 0 , 0 , 0 , 0 ,
            -10, 0 , 0 , 0 , 0 ,-10,
            0 , 0 ,15 ,15 , 0 , 0 
        ]

        self.knightEvalWhite2 = [
            -50,-40,-30,-30,-40,-50,
            -40,-20, 0 , 0 ,-20,-40,
            -30, 5 , 15, 15, 5 ,-30,
            -30, 5 ,-5 ,-5 , 5 ,-30,
            -40,-20, 5 , 5 , 5 ,-40,
            -50,-40,-30,-30,-40,-50,  
        ]

        self.bishopEvalWhite2 = [
            -20,-10,-10,-10,-10,-20,
            -10, 0 , 0 , 0 , 0,-10,
            -10, 5 , 10, 10, 5 ,-10,
            -10, 5 , 5 , 5 , 10,-10,
             5 , 0 , 10, 10, 5 , 5 ,
            -50,-40,-30,-30,-40,-50,  
        ]

        self.kingEvalWhite2 = [
            -30,-40,-50,-50,-40,-30,
            -30,-40,-50,-50,-40,-30,
            -30,-40,-50,-50,-40,-30,
            -20,-20,-20,-20,-20,-10,
            20, 15,-5 ,-5 , 15, 20,
            50, 10, 5 , 5 , 10, 50,  
        ]

        #Evaluation array for white pieces
        self.pawnEvalWhite = [
            0.0,  0.0,  0.0,  0.0,  0.0,  0.0,
            5.0,  5.0,  5.0,  5.0,  5.0,  5.0,
            1.5,  2.5,  3.5,  3.5,  2.5,  1.5,
            0.0,  0.0,  0.0,  0.0,  0.0,  0.0,
            0.5,  1.0, -2.0, -2.0,  1.0,  0.5,
            0.0,  0.0,  0.0,  0.0,  0.0,  0.0,
        ]

        self.rookEvalWhite = [
            0.0,  0.0,  0.0,  0.0,  0.0,  0.0,
            -0.5,  1.0,  1.0,  1.0,  1.0, -0.5,
            -0.5,  0.0,  0.0,  0.0,  0.0, -0.5,
            -0.5,  0.0,  0.0,  0.0,  0.0, -0.5,
            -0.5,  0.0,  0.0,  0.0,  0.0, -0.5,
            0.0,  0.0,  1.0,  1.0,  0.0,  0.0,
        ]

        self.knightEvalWhite = [
            -5.0, -2.0, -1.0, -1.0, -2.0, -5.0,
            -3.0, -2.0,  0.5,  0.5,  0.0, -3.0,
            -2.0,  1.0,  2.0,  2.0,  1.0,  0.0,
            -2.0,  1.0,  2.0,  2.0,  1.0,  0.5,
            -3.0,  0.0,  0.5,  0.5,  0.0, -3.0,
            -5.0, -2.0, -1.0, -1.0, -2.0, -5.0,
        ]

        self.bishopEvalWhite = [
            -2.0, -1.0, -1.0, -1.0, -1.0, -2.0,
            -1.0,  0.0,  0.0,  0.0,  0.0, -1.0,
            -1.0,  0.5,  0.0,  0.0,  0.5, -1.0,
            -1.0,  1.0,  1.0,  1.0,  1.0, -1.0,
            -1.0,  0.5,  0.0,  0.0,  0.5, -1.0,
            -2.0, -1.0, -1.0, -1.0, -1.0, -2.0,
        ]

        self.kingEvalWhite = [
            -4.0, -4.0, -5.0, -5.0, -4.0, -4.0,
            -3.0, -4.0, -5.0, -5.0, -5.0, -3.0,
            -2.5, -3.0, -4.0, -4.0, -3.0, -2.5,
            -1.5, -2.0, -2.0, -2.0, -2.0, -1.5,
            2.0,  2.0,  0.0,  0.0,  2.0,  2.0,
            2.0,  3.0,  1.0,  1.0,  3.0,  2.0,
        ]

        #Evaluation array for black pieces
        self.pawnEvalBlack = self.reverseArray(self.pawnEvalWhite)
        self.rookEvalBlack = self.reverseArray(self.rookEvalWhite)
        self.knightEvalBlack = self.reverseArray(self.knightEvalWhite)
        self.bishopEvalBlack = self.reverseArray(self.bishopEvalWhite)
        self.kingEvalBlack = self.reverseArray(self.kingEvalWhite)

        #total evaluation values per piece
        self.evaluationValuesOfPieces = {'p': 10,
                                        'N': 40,
                                        'B': 30,
                                        'R': 50,
                                        'K': 0}
        #and their positions
        self.validationArrayOfPieces = {'wp': self.pawnEvalWhite,
                                        'wN': self.knightEvalWhite,
                                        'wB': self.bishopEvalWhite,
                                        'wR': self.rookEvalWhite,
                                        'wK': self.kingEvalWhite,
                                        'bp': self.pawnEvalBlack,
                                        'bN': self.knightEvalBlack,
                                        'bB': self.bishopEvalBlack,
                                        'bR': self.rookEvalBlack,
                                        'bK': self.kingEvalBlack}



    def get_move(self):
        move = None
        
        while not self.move_queue.empty():
            move = self.move_queue.get()
        return move

    def update_move(self, move, score, depth):
        self.move_queue.put([move, score, depth])

    def clear_queue(self, outer_queue):
        self.move_queue = outer_queue


    def findBestMove(self, gs):
        """
        Helper method to make the agent find the best move.
        
        Parameters
        ----------
        gs : GameState
            The current state of the game.

        Returns
        -------
        None

        """
        
        #Get playing color of Agent
        if gs.whiteToMove:
            self.color = 'white'
        else:
            self.color = 'black'

        #Start timer
        self.start = datetime.datetime.now()
        self.timeout = self.start + datetime.timedelta(seconds=19)

        #Set depth
        self.depth = 4
        copyGS = copy.deepcopy(gs)

        #Start alpha beta search
        (bestScore, bestMove) = self.alphaBetaMax(copyGS,-float('inf'), float('inf'), self.depth)
        print('Alpha cutoffs %d and Beta cutoffs %d ', self.alphaCutOffCounter, self.betaCutOffCounter)
        #return best move as update_move
        self.update_move(bestMove, bestScore, self.depth)
        
        
#-------Alpha Beta Search Algorithm-------#

    def alphaBetaMax(self, gs, alpha, beta, depth):
        """
        Helper method to make the agent find the best move.
        
        Parameters
        ----------
        gs : GameState
            The current state of the game.
        alpha : float
            The alpha value for the alpha beta pruning.
        beta : float
            The beta value for the alpha beta pruning.
        depth : int
            The depth of the alpha beta search.

        Returns
        -------
        (float, Move)
            The best score and the best move.

        """

        
        
       #check for terminal node and timeout
        if depth == 0 or gs.checkMate or gs.staleMate or gs.threefold or gs.draw or datetime.datetime.now() > self.timeout:
            #return self.Quiesce(gs,alpha,beta,depth,2)
            return (self.evaluateBoard(gs), None)

        #Get all valid moves
        validMoves = gs.getValidMoves()
        #pre sort valid moves
        validMoves = self.moveOrdering(validMoves, gs)

        if len(validMoves) == 0:
            return (self.evaluateBoard(gs), None)

        bestScore = None
        bestMove = None

        #Loop through all valid moves
        for move in validMoves:

            #make move
            gs.makeMove(move)
            #get score
            (score, nextMove) = self.alphaBetaMin(gs, alpha, beta, depth-1)
            #undo move
            gs.undoMove()

            #pruning and cut offs
            if score >= beta:
                self.betaCutOffCounter += 1
                return (score, move)

            if score > alpha:
                alpha = score

            #init best move
            if bestMove == None:
                bestMove = move
                bestScore = score
            
            elif score > bestScore:
                #update best move
                bestMove = move
                bestScore = score

        return (bestScore, bestMove)

    def alphaBetaMin(self, gs, alpha, beta, depth):
        """
        Helper method to make the agent find the best move.
        
        Parameters
        ----------
        gs : GameState
            The current state of the game.
        alpha : float
            The alpha value for the alpha beta pruning.
        beta : float
            The beta value for the alpha beta pruning.
        depth : int
            The depth of the alpha beta search.

        Returns
        -------
        (float, Move)
            The best score and the best move.

        """
        
        #check for terminal node and timeout
        if depth == 0 or gs.checkMate or gs.staleMate or gs.threefold or gs.draw or datetime.datetime.now() > self.timeout:
            #return self.Quiesce(gs,alpha,beta,depth,1)
            return (self.evaluateBoard(gs), None)

        #Get all valid moves
        validMoves = gs.getValidMoves()
        #pre sort valid moves
        validMoves = self.moveOrdering(validMoves, gs)

        if len(validMoves) == 0:
            return (self.evaluateBoard(gs), None)

        bestScore = None
        bestMove = None

        #Loop through all valid moves
        for move in validMoves:

            #make move
            gs.makeMove(move)
            #get score
            (score, nextMove) = self.alphaBetaMax(gs, alpha, beta, depth-1)
            #undo move
            gs.undoMove()

            #pruning and cut offs
            if score <= alpha:
                self.alphaCutOffCounter += 1
                return (score, move)

            if score < beta:
                beta = score

            #init best move
            if bestMove == None:
                bestMove = move
                bestScore = score
            
            elif score < bestScore:
                #update best move
                bestMove = move
                bestScore = score

        return (bestScore, bestMove)


#-------Move Ordering Functions-------#

    def moveOrdering(self, validMoves, gs):
        """
        Helper method to make the agent find the best move.
        
        Parameters
        ----------
        validMoves : list
            The list of valid moves.
        gs : GameState
            The current state of the game.

        Returns
        -------
        list
            The list of valid moves.

        """
        
        #get value of current GameState
        currentValue = self.evaluateBoard(gs)

        #sort valid moves
        return sorted(validMoves, key=lambda move: self.evaluateMove(gs, move, currentValue), reverse=True)
        

#-------Evaluation Functions-------#

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

        for i in range(36):
            materialScore = 0
            positionScore = 0
            mobilityScore = 0
            figure = gs.board[i]

            if figure[0] == 'w':
                factor = 1
            else:
                factor = -1

            if figure != '--':
                #score = factor *self.evalMaterialOfFigure(figure[1])
                materialScore = self.evalMaterialOfFigure(figure[1])
                positionScore = materialScore * self.evalPositionOfFigure(figure, i)
                mobilityScore = self.evalMobilityOfFigure(gs,figure[1], i)

                score += factor * (materialScore + 0.3*positionScore + 0.5*mobilityScore)


        #check which color is to move
        #because after move gs.whiteToMove is switched
        if self.color == 'white':
            return score
        else:
            return -score   

    def evaluateBoardShort(self, gs):
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

        for i in range(36):

            figure = gs.board[i]

            if figure[0] == 'w':
                factor = 1
            else:
                factor = -1

            if figure != '--':
                score += factor*self.evalMaterialOfFigure(figure[1])
                

        #check which color is to move
        #because after move gs.whiteToMove is switched
        if self.color == 'white':
            return score
        else:
            return -score

    def evalMaterialOfFigure(self, figure):
        """
        Evaluate the material of a figure

        Parameters
        ----------
        figure : str
            figure to be evaluated
        index : int
            index of the figure

        Returns
        -------
        int

        """
        return self.evaluationValuesOfPieces[figure]

    def evalMobilityOfFigure(self, gs, figure ,index):
        """
        Evaluate mobility on board

        Parameters
        ----------
        gs : GameState
            gamestate to be evaluated
        figure : str
            figure to be evaluated
        index : int 
            index of position on board
        Returns
        -------
        int

        """
        
        pos = self.getPositionOfIndex(index)

        rc = pos[0] * 6 + pos[1]

        pM = nM = bM = rM = kM = []


        if figure == 'p':    #if 5< index < 30  pawn has no possible moves
            try:
                gs.getPawnMoves(pos[0], pos[1] ,pM)
            except:
                return 0
                #print('pawn')
                #print('index', index)
                #print(gs.board)  
                
            return len(pM)
        elif figure == 'N':
            gs.getKnightMoves(pos[0], pos[1] ,nM)
            return len(nM)
        elif figure == 'B':
            gs.getBishopMoves(pos[0], pos[1] ,bM)
            return len(bM)
        elif figure == 'R':
            gs.getRookMoves(pos[0], pos[1] ,rM)
            return len(rM)
        elif figure == 'K':
            gs.getKingMoves(pos[0], pos[1] ,kM)
            return len(kM)
        else:
            return 0

    def evalPositionOfFigure(self, figure, index):
        """
        Evaluate position on board

        Parameters
        ----------
        figure : str
            figure on index
        index : int
            index of position on board

        Returns
        -------
        int

        """
        return self.validationArrayOfPieces[figure][index]    

    def evalEndingGame(self, gs):
        """
        Evaluate the end of the game

        Parameters
        ----------
        gs : GameState
            gamestate to be evaluated

        Returns
        -------
        int

        """
        score = 0
        #check if game is over
        if gs.checkMate:
            #check if won or lost
            if gs.whiteToMove:
                #white won
                if self.color == 'white':
                    #we won
                    score = 100000
                else:
                    #we lost
                    score = -100000

            else:
                #black won
                if self.color == 'white':
                    #we lost
                    score = -100000
                else:
                    #we won
                    score = 100000

    def evaluateMove(self, gs, move, currentValue):
        """
        Helper method to make the agent find the best move.
        
        Parameters
        ----------
        gs : GameState
            The current state of the game.
        move : Move
            The move to evaluate.
        currentValue : float
            The value of the current GameState.

        Returns
        -------
        float
            The value of the move.

        """
        
        #make move
        gs.makeMove(move)
        #get value of move
        valueAfterMove = self.evaluateBoardShort(gs)
        #undo move
        gs.undoMove()

        return valueAfterMove - currentValue


#-------Helper Functions-------#

    def reverseArray(self,array):
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

    def getPositionOfFigure(self, gs, figure):
        """
        Get the position of the figure

        Parameters
        ----------
        gs : GameState
            gamestate to access board
        figure : str
            figure to find position of

        Returns
        -------
        list with tupels (r,c)
            

        """
        list = []
        for i in range(0, 35):
            if gs.board[i] == figure:
                # row = i % 6  -> modulo 6
                # col = i // 6  -> divide by 6 without remainder
                list.append((i % 6, i // 6))

        return list

    def getPositionOfIndex(self,index):
        """
        Get the position of the figure

        Parameters
        ----------
        index : int
            index to find position of

        Returns
        -------
        list with tupels (r,c)
            

        """
        return  (index // 6,index % 6)

    def getIndexOfPosition(gs, posList):
        """
        Get the index of a position in the board

        Parameters
        ----------
        gs : GameState
            gamestate to be evaluated
        posList : list
            list of position (r,c)

        Returns
        -------
        int: index

        """
        index = 0
        #add row
        index += posList[0]
        #add col
        index += posList[1]*6

        return index






