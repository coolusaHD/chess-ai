import random
import datetime
import copy
import hashlib
from ChessEngine import Move

class Agent:
    def __init__(self):

        self.move_queue = None
        self.nextMove = None
        self.counter = None
        self.currentDepth = None
        self.start = None
        self.timeout = None

        self.globalBestMove = None
        self.globalBestScore = 0
        self.globalBestDepth = 0
        #startinf depth
        self.depth = 0
        self.color = None
        self.alphaCutOffCounter = 0
        self.betaCutOffCounter = 0
        self.tableCounter = 0

        

        #self.zobristTable = self.initZobristTable()
        self.hashedBoard = None
        self.hashStorageTable = {}


        #---------Evaluation Values---------

        #mobility base value
        self.mobilityEvaluationBaseValue = 10

        #ending game values
        self.checkEval = 20
        self.checkMateEval = 10000

        #Evaluation array for white pieces
        self.pawnEvalWhite= [
            5, 5, 5, 5, 5, 5,
            5, 6, 7, 7, 6, 5,
            0, 0, 8, 8, 0, 0,
            0, 0, 7, 7, 0, 0,
            5, 6, -5, -5, 6,5,
            0, 0, 0, 0, 0, 0]

        self.rookEvalWhite = [
            0, 0, 0, 0, 0, 0,
            0, 10, 10, 10, 10, 0,
            0, 1, 1, 1, 1, 0,
            0, 1, 1, 1, 1, 0,
            0, 1, 1, 1, 1, 0,
            0, 0, 5, 5, 0, 0]

        self.knightEvalWhite = [
            -20, -15, -10, -10, -15, -20,
            -15, -10, 0, 0, -5, -5,
            -10, 0, 8, 8, 0, -5,
            -10, 0, 8, 8, 0, -5,
            -5, -4, 5, 5, -4, -5,
            -8, -4, -4, -4, -4, -8]

        self.bishopEvalWhite = [
            -10, -5, -5, -5, -5, -10,
            -10, 0, 0, 0, 0, -10,
            -3, 0, 6, 6, 0, -3,
            -3, 6, 6, 6, 6, -3,
            -3, 5, 0, 0, 5, -3,
            -10, -5, -5, -5, -5, -10]

        self.kingEvalWhite = [
            -6, -6, -6, 6, -6, -6,
            -6, -6, -6, -6, -6, -6,
            -6, -6, -6, -6, -5, -6,
            -5, -6, -6, -6, -6, -5,
            20, 20, 0, 0, 20, 20,
            20, 25, 0, 0, 25, 20]


        #Evaluation array for black pieces
        self.pawnEvalBlack = self.reverseArray(self.pawnEvalWhite)
        self.rookEvalBlack = self.reverseArray(self.rookEvalWhite)
        self.knightEvalBlack = self.reverseArray(self.knightEvalWhite)
        self.bishopEvalBlack = self.reverseArray(self.bishopEvalWhite)
        self.kingEvalBlack = self.reverseArray(self.kingEvalWhite)

        #total evaluation values per piece
        self.evaluationValuesOfPieces = {'p': 10,
                                        'N': 50,
                                        'B': 40,
                                        'R': 60,
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
        #Start timer
        self.start = datetime.datetime.now()
        self.timeout = self.start + datetime.timedelta(seconds=18)
        
        #Get playing color of Agent
        if gs.whiteToMove:
            self.color = 'white'
        else:
            self.color = 'black'

        #hash board for first time
        self.hashedBoard = self.hashBoard(gs)
        
        #Opening Book
        openingScore = None
        openingMove = None
        
        if len(gs.moveLog) == 0:
            (openingScore, openingMove) = self.openingBookWhite(gs)
        elif len(gs.moveLog) == 1:
            (openingScore, openingMove) = self.openingBookBlack(gs)
        

        if openingScore != None:
            self.globalBestMove = openingMove
            self.globalBestScore = openingScore
        #After two moves run normal
        else: 

            #itertive deepening
            while datetime.datetime.now() < self.timeout:
                self.depth += 1

                (bestScore, bestMove) = self.alphaBetaMax(gs,-100000, 100000, self.depth)
                
                print('Actual Data: Depth: ' + str(self.depth) + ' Best Score: ' + str(bestScore) + ' Best Move: ' + str(bestMove))
                print('Alpha CO: %d Beta CO: %d and Table counter: %d' % (self.alphaCutOffCounter, self.betaCutOffCounter, self.tableCounter))
                print('Time: ' + str(datetime.datetime.now() - self.start))

                if bestScore != None :
                    self.globalBestScore = bestScore
                    self.globalBestMove = bestMove
                    self.globalBestDepth = self.depth

        #return best move as update_move
        #print('Im taking this move: ' + str(self.globalBestMove))
        self.update_move(self.globalBestMove, self.globalBestScore, self.globalBestDepth)
        
        
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
            #return (self.Quiesce(gs,alpha,beta,depth,2), None)
            return (self.evaluateBoard(gs), None)

        #Get all valid moves
        try:
            validMoves = gs.getValidMoves()
        except:
            print(gs.board)
            validMoves = []

        if len(validMoves) == 0:
            return (self.evaluateBoard(gs), None)

        #pre sort valid moves
        validMoves = self.moveOrdering(validMoves, gs)

        bestScore = None
        bestMove = None

        #Loop through all valid moves
        for move in validMoves:

            #make move
            gs.makeMove(move)
            #self.hashedBoard = self.updatezTableFromMove(self.hashedBoard, move)
            #get score
            (score, nextMove) = self.alphaBetaMin(gs, alpha, beta, depth-1)
            #undo move
            gs.undoMove()
            #self.hashedBoard = self.undoUpdatezTableFromMove(self.hashedBoard, move)

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
            #return (self.Quiesce(gs,alpha,beta,depth,2), None)
            return (self.evaluateBoard(gs), None)

        #Get all valid moves
        try:
            validMoves = gs.getValidMoves()
        except:
            print(gs.board)
            validMoves = []

        if len(validMoves) == 0:
            return (self.evaluateBoard(gs), None)

        #pre sort valid moves
        validMoves = self.moveOrdering(validMoves, gs)

        bestScore = None
        bestMove = None

        #Loop through all valid moves
        for move in validMoves:

            #make move
            gs.makeMove(move)
            #self.hashedBoard = self.updatezTableFromMove(self.hashedBoard, move)
            #get score
            (score, nextMove) = self.alphaBetaMax(gs, alpha, beta, depth-1)
            #undo move
            gs.undoMove()
            #self.hashedBoard = self.undoUpdatezTableFromMove(self.hashedBoard, move)

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

    def Quiesce(self, gs, alpha, beta, depth , depthLeft):
        """
        Quiescence search

        Parameters
        ----------
        gs : GameState
            gamestate to access board
        alpha : float
            alpha value
        beta : float
            beta value
        depth : int
            depth of recursion
        depthLeft : int 
            depth left for recursion

        Returns
        -------
        float

        """
        stand_pat = self.evaluateBoard(gs)

        #check for endgame
        if depthLeft == 0 or gs.checkMate or gs.staleMate or gs.threefold or gs.draw:
            #print('returning from endgame')
            return stand_pat

        if(stand_pat >= beta):
            return beta
        if(alpha < stand_pat):
            alpha = stand_pat
        #consider every capture
        validMoves= []
        try:
            validMoves = gs.getValidMoves()

        except:
            return alpha

        for move in validMoves:
            if move.isCapture:
                gs.makeMove(move)
                score = -self.Quiesce(gs, -beta, -alpha ,depth, depthLeft-1)
                gs.undoMove()
                if(score >= beta):
                    return beta
                if(score > alpha):
                    alpha = score
        return alpha

#---------Hashing functions--------# deprecated

    #def indciesOfFigures(self, string):
        """
        Helper method to get indices of figures

        Parameters
        ----------
        string : str
            string to be evaluated

        Returns
        -------
        int
            index of figure

        """

        dictOfFigures = {'bp': 0, 'bN': 1, 'bB': 2, 'bR': 3, 'bK': 4, 'wp': 5, 'wN': 6, 'wB': 7, 'wR': 8, 'wK': 9, '--': 10}

        return dictOfFigures[string]
        
    #def figureStringFromIndicies(self, num):
        """
        Helper method to get figure string from index

        Parameters
        ----------
        num : int
            index

        Returns
        -------
        str

        """

        dictOfNums = {0: 'bp', 1: 'bN', 2: 'bB', 3: 'bR', 4: 'bK', 5: 'wp', 6: 'wN', 7: 'wB', 8: 'wR', 9: 'wK' , 10: '--'}

        return dictOfNums[num]

    #def initZobristTable(self):
        """
        Helper method to initialize the Zobrist table

        Returns
        -------
        list

        """
        table = []
        for i in range(36):
            table.append([])
            for j in range(11):
                table[i].append(random.randint(0, 2**64 - 1))
        return table

    def hashBoard(self, gs):
        """
        Helper method to hash the board

        Parameters
        ----------
        gs : GameState
            gamestate to access board

        Returns
        -------
        int : hash of board

        """
        return int(hashlib.md5(str(gs.board).encode('utf-8')).hexdigest(), 16)

    #def updatezTableFromMove(self, hash, move):
        """
        Helper method to update the zobrist table after a move

        Parameters
        ----------
        gs : GameState
            gamestate to access board
        move : Move
            move to be evaluated

        Returns
        -------
        new hash

        """
        #update zobrist table from start and end position of move
        startPos = move.startRC
        endPos = move.endRC
        movingfigure = move.pieceMoved
        capturedFigure = move.pieceCaptured

        #print('capturedFig',capturedFigure)
        #print('hb', hash)

        #remove moving figure from start pos
        hash ^= self.zobristTable[startPos][self.indciesOfFigures(movingfigure)]
        #add empty field at start pos
        hash ^= self.zobristTable[startPos][self.indciesOfFigures('--')]
        #remove capturing figure
        hash ^= self.zobristTable[endPos][self.indciesOfFigures(capturedFigure)]
        #adding moving figure to his new position
        hash ^= self.zobristTable[endPos][self.indciesOfFigures(movingfigure)]

        return hash

    #def undoUpdatezTableFromMove(self, hash, move):
        """
        Helper method to undo the update of the zobrist table after a move

        Parameters
        ----------
        gs : GameState
            gamestate to access board
        move : Move
            move to be evaluated

        Returns
        -------
        new hash

        """
        #update zobrist table from start and end position of move
        startPos = move.startRC
        endPos = move.endRC
        movingfigure = move.pieceMoved
        capturedFigure = move.pieceCaptured

        #print('capturedFig',capturedFigure)
        #print('hb', hash)

        #remove moving figure from end pos
        hash ^= self.zobristTable[endPos][self.indciesOfFigures(movingfigure)]
        #remove empty field at start pos
        hash ^= self.zobristTable[startPos][self.indciesOfFigures('--')]
        #add captured figure
        hash ^= self.zobristTable[endPos][self.indciesOfFigures(capturedFigure)]
        #adding moving figure to his old position
        hash ^= self.zobristTable[startPos][self.indciesOfFigures(movingfigure)]

        return hash


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
        currentValue = self.evaluateBoardShort(gs)

        #sort valid moves
        return sorted(validMoves, key=lambda move: self.evaluateMove(gs, move, currentValue), reverse=True)
        

#-------Evaluation Functions-------#

    def checkForSavedEvaluation(self,gs):
        """
        Check if a gamestate has been evaluated before

        Parameters
        ----------
        gs : GameState
            gamestate to be evaluated

        Returns
        -------
        int: saved evaluation
        or
        None    

        """
        #check if evaluated gamestate is in table
        #get item from table
        self.hashedBoard = self.hashBoard(gs)
        maybeSavedEntry = self.hashStorageTable.get(self.hashedBoard)

        if maybeSavedEntry != None:
            #print('returning from table')
            self.tableCounter += 1
            savedEvaluation = maybeSavedEntry['score']
            return savedEvaluation 
        else:
            return None

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

        #check if evaluated gamestate is in table

        maybeSavedEvaluation = self.checkForSavedEvaluation(gs)

        if maybeSavedEvaluation != None:
            score = maybeSavedEvaluation
        
        else:
            score = 0
            for i in range(36):

                figure = gs.board[i]
                if figure == '--':
                    continue

                materialScore = 0
                positionScore = 0
                mobilityScore = 0

                if figure[0] == 'w':
                    factor = 1
                else:
                    factor = -1

                #score = factor *self.evalMaterialOfFigure(figure[1])
                materialScore = self.evalMaterialOfFigure(figure[1])
                positionScore = self.evalPositionOfFigure(figure, i)
                mobilityScore = self.evalMobilityOfFigure(gs,figure[1], i)

                score += factor * (materialScore*1.2 + positionScore + mobilityScore*0.3)

            #evaluate endgame
            endingGameScore = self.evalEndingGame(gs)

            score += endingGameScore
            
            self.hashedBoard = self.hashBoard(gs)
            #save evaluation in table
            self.hashStorageTable[self.hashedBoard] = {'score': score}

        #check which color is to move
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
            if figure == '--':
                continue

            if figure[0] == 'w':
                factor = 1
            else:
                factor = -1

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
            return self.mobilityEvaluationBaseValue *(len(nM)/8)
        elif figure == 'B':
            gs.getBishopMoves(pos[0], pos[1] ,bM)
            return self.mobilityEvaluationBaseValue *(len(bM)/9)
        elif figure == 'R':
            gs.getRookMoves(pos[0], pos[1] ,rM)
            return self.mobilityEvaluationBaseValue *(len(rM)/10)
        elif figure == 'K':
            gs.getKingMoves(pos[0], pos[1] ,kM)
            return self.mobilityEvaluationBaseValue *(len(kM)/8)
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
        #check if game is over
        if gs.checkMate:
            #check if won or lost
            if gs.whiteToMove:
                #white lost
                return -self.checkMateEval
            else:
                #white won
                return self.checkMateEval
        else:
            return 0

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


#-------Opening Book Functions-------#

    def openingBookWhite(self,gs):

        # because white is the one to open, we just return a favourable opening move
        openingMove = Move((4, 2),(3, 2), gs.board)
        return (-1, openingMove)

    def openingBookBlack(self,gs):
        openingMove = gs.moveLog[-1].getChessNotation()
        
        responseDict = {}
        # -- whtie moved knight
        # respond with c5c4
        responseDict['c1b3'] = Move((1, 2), (2, 2), gs.board)
        responseDict['c1d3'] = Move((1, 2), (4, 0), gs.board)
        # -- whtie moved pawn
        # respond with c5c4
        responseDict.update(dict.fromkeys(['a2a3', 'c2c3', 'e2e3', 'f2f3'], Move((1, 2), (2, 2), gs.board)))
        # respond with b5b4
        responseDict['b2b3'] = Move((1, 1), (2, 1), gs.board)
        # respond with d5d4
        responseDict['d2d3'] = Move((1, 3), (2, 3), gs.board)



        # if something went wrong
        if not openingMove in responseDict or not responseDict[openingMove] in gs.getValidMoves():
            return (-1, Move((1, 2), (2, 2), gs.board))

        return (-1, responseDict[openingMove])


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
        index += posList[0]*6
        #add col
        index += posList[1]

        return index






