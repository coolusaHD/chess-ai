import random
import time
import copy
import datetime
from typing import ChainMap

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

        self.zobristTable = self.initZobristTable()
        self.hashedBoard = None
        self.hashStorageTable = {}

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
        self.timeout = self.start + datetime.timedelta(seconds=19)

        self.hashedBoard = self.hashBoard(gs) 


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
            print('Table counter: ', self.tableCounter)

        #return best move as update_move
        self.update_move(self.globalBestMove, self.globalBestScore, self.currentDepth)
            

    def indciesOfFigures(self, string):
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
        
    def figureStringFromIndicies(self, num):
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

    def initZobristTable(self):
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
        int

        """
        hash = 0
        for i in range(36):
            hash ^= self.zobristTable[i][self.indciesOfFigures(gs.board[i])]
        return hash

    def updatezTableFromMove(self, hash, move):
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
        figure = move.pieceMoved
        capturedFigure = move.pieceCaptured

        #print('capturedFig',capturedFigure)
        #print('hb', hash)

        #remove moving figurefrom start pos
        hash ^= self.zobristTable[startPos][self.indciesOfFigures(figure)]
        #add empty field at start pos
        hash ^= self.zobristTable[startPos][self.indciesOfFigures('--')]
        #remove capturing figure
        hash ^= self.zobristTable[endPos][self.indciesOfFigures(capturedFigure)]
        #adding moving figure to his new position
        hash ^= self.zobristTable[endPos][self.indciesOfFigures(figure)]

        return hash

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


        #get all valid moves
        validMoves = gs.getValidMoves()

          #check for timeout
        if datetime.datetime.now() > self.timeout:
            return None
         #check for endgame
        if depth == 0 or gs.checkMate or gs.staleMate or gs.threefold or gs.draw:
            return self.Quiesce(gs,alpha,beta,depth)

        #check for maxPlayer
        if maxPlayer:

            #move ordering for maxPlayer
            validMoves = self.moveOrdering( gs, validMoves)

            #check for maxPlayer
            #bestScore = -float('inf')
            score = -float('inf')

            #iterate over all valid moves
            for move in validMoves:

                #copy gamestate
                copyGS = copy.deepcopy(gs)
                #make move
                copyGS.makeMove(move)
                #recursive call
                score = self.alphaBeta(copyGS, depth - 1, alpha, beta, False)

                #update score
                #bestScore = max(bestScore, score)
                #update alpha
                #alpha = max(alpha, bestScore)
                if score is None:
                    return alpha
                alpha = max(alpha, score)

                #check for beta cut off
                if beta <= alpha:
                    self.beta_cutoff_counter += 1
                    break

            return score

        #check for minPlayer
        else:

            #move ordering for minPlayer
            validMoves = self.moveOrdering(gs,validMoves)

            #check for minPlayer
            #bestScore = float('inf')
            score = float('inf')

            #iterate over all valid moves
            for move in validMoves:

                #copy gamestate
                copyGS = copy.deepcopy(gs)
                #make move
                copyGS.makeMove(move)
                #recursive call
                score = self.alphaBeta(copyGS, depth - 1, alpha, beta, True)

                #update score
                #bestScore = min(bestScore, score)
                #update beta
                if score is None:
                    return beta
                beta = min(beta, score)

                #check for alpha cut off
                if beta <= alpha:
                    self.alpha_cutoff_counter += 1
                    break

            return score 

    def Quiesce(self, gs, alpha, beta, depth):
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

        Returns
        -------
        float

        """
        #check for timeout
        if datetime.datetime.now() > self.timeout:
            return False

        #check if evaluated gamestate is in table
        #hash actual board
        
        actualBoardHashed = self.updatezTableFromMove(self.hashedBoard ,gs.moveLog[-1])
        
        #get item from table
        maybeSavedEntry = self.hashStorageTable.get(actualBoardHashed)

        if maybeSavedEntry != None:
            #print('returning from table')
            self.tableCounter += 1
            stand_pat = maybeSavedEntry['score']
        
        else:
            stand_pat = self.evaluateBoard(gs)
            #save score of gamestate in table
            self.hashStorageTable[actualBoardHashed] = {'score': stand_pat, 'depth': depth}

        if(stand_pat >= beta):
            return beta
        if(alpha < stand_pat):
            alpha = stand_pat
        #consider every capture
        validMoves = gs.getValidMoves()
        for move in validMoves:
            if move.isCapture:
                gs.makeMove(move)
                score = -self.Quiesce(gs, -beta, -alpha ,depth)
                gs.undoMove()
                if(score >= beta):
                    return beta
                if(score > alpha):
                    alpha = score
        return alpha

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
    evaluationValuesOfPieces = {'p': 10, 'N': 28, 'B': 30, 'R': 40, 'K': 0}

    checkEval = 20
    checkMateEval = 10000

    #Evaluation array for white pieces
    pawnEvalWhite = [
        0 , 0 , 0 , 0 , 0 , 0 ,
        50, 50, 50, 50, 50, 50,
        20, 20, 30, 30, 20, 20,
        15, 0 , 20, 20, 10, 5 ,
        5 , 10,-20,-20, 10, 5 ,
        0 , 0 , 0 , 0 , 0 , 0  
    ]

    rookEvalWhite = [
        0 , 0 , 0 , 0 , 0 , 0 ,
        5 ,10 ,10 ,10 ,10 , 5 ,
        0 , 0 , 0 , 0 , 0 , 0 ,
        0 , 0 , 0 , 0 , 0 , 0 ,
       -10, 0 , 0 , 0 , 0 ,-10,
        0 , 0 ,15 ,15 , 0 , -5 
    ]

    knightEvalWhite = [
       -50,-40,-30,-30,-40,-50,
       -40,-20, 0 , 0 ,-20,-40,
       -30, 5 , 15, 15, 5 ,-30,
       -30, 5 ,-5 ,-5 , 5 ,-30,
       -40,-20, 5 , 5 , 5 ,-40,
       -50,-40,-30,-30,-40,-50,  
    ]

    bishopEvalWhite = [
       -20,-10,-10,-10,-10,-20,
       -10, 0 , 0 , 0 , 0,-10,
       -10, 5 , 10, 10, 5 ,-10,
       -10, 5 , 5 , 5 , 10,-10,
        5 , 0 , 10, 10, 5 , 5 ,
       -50,-40,-30,-30,-40,-50,  
    ]

    kingEvalWhite = [
       -30,-40,-50,-50,-40,-30,
       -30,-40,-50,-50,-40,-30,
       -30,-40,-50,-50,-40,-30,
       -20,-20,-20,-20,-20,-10,
        20, 15, 0 , 0 , 15, 20,
        50, 10, 5 , 5 , 10, 50,  
    ]

    #Evaluation array for black pieces
    pawnEvalBlack = reverseArray(pawnEvalWhite)
    rookEvalBlack = reverseArray(rookEvalWhite)
    knightEvalBlack = reverseArray(knightEvalWhite)
    bishopEvalBlack = reverseArray(bishopEvalWhite)
    kingEvalBlack = reverseArray(kingEvalWhite)

    validationArrayOfPieces = {'wp': pawnEvalWhite, 'wN': knightEvalWhite, 'wB': bishopEvalWhite, 'wR': rookEvalWhite, 'wK': kingEvalWhite, 'bp': pawnEvalBlack, 'bN': knightEvalBlack, 'bB': bishopEvalBlack, 'bR': rookEvalBlack, 'bK': kingEvalBlack}


#------Position translator functions ------


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
   


#-------Evaluation functions-------

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

        for i in range(36):
            figure = gs.board[i]

            if figure[0] == 'w':
                factor = 1
            else:
                factor = -1

            if figure != '--':
                #score = factor *self.evalMaterialOfFigure(figure[1])
                materialScore = self.evalMaterialOfFigure(figure[1])
                positionScore = self.evalPositionOfFigure(figure, i)
                mobilityScore = self.evalMobilityOfFigure(gs,figure[1], i)
                score += factor * (materialScore + 0.25*positionScore + 0.5*mobilityScore)


        #check for good and bad captures
        if gs.moveLog[-1] != None:
            score += self.evalCapture(gs.moveLog[-1])

        #check which color is to move
        #because after move gs.whiteToMove is switched
        if self.color == 'white':
            return score
        else:
            return -score

    def evalKingSafety(self, gs):
        """
        Evaluate the king safety 

        Parameters
        ----------
        gs : GameState
            gamestate to be evaluated

        Returns
        -------
        int

        """
        scoreW = 0
        scoreB = 0

        #get position of kings
        
        whiteKingPos = gs.blackKingLocation
        blackKingPos = gs.blackKingLocation

        rowbK, colbK = whiteKingPos[0], whiteKingPos[1]
        rowwK, colwK = blackKingPos[0], blackKingPos[1]

        
        #check for king safety

        if gs.squareUnderAttack(rowbK, colbK):
            scoreW += 2*self.pawnSingleEval
        else:
            scoreW -= self.pawnSingleEval/2
        
        if gs.squareUnderAttack(rowwK, colwK):
            scoreB += 2*self.pawnSingleEval
        else:
            scoreB -= self.pawnSingleEval/2

            
        return scoreW-scoreB

    def evalCapture(self,move):
        """
        Evaluate the capture of a figure

        Parameters
        ----------
        move : Move
            capture move to be evaluated

        Returns
        -------
        int

        """
        score = 0


        if move.isCapture:

            movingFigure = move.pieceMoved
            capturedFigure = move.pieceCaptured

            #print(movingFigure, capturedFigure)

            if movingFigure[1] == '-':
                print('something went wrong')
                return 0
            movingFigureValue = self.evalMaterialOfFigure(movingFigure[1])
            capturedFigureValue = self.evalMaterialOfFigure(capturedFigure[1])

            if movingFigureValue < capturedFigureValue:
                score += (capturedFigureValue - movingFigureValue)*0.5

            if movingFigureValue > capturedFigureValue:
                score -= (capturedFigureValue - movingFigureValue)*0.5

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
            score -= self.checkMateEval

        return score

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

        if figure == 'p':
            pM = []
            gs.getPawnMoves(pos[0], pos[1] ,pM)
            return len(pM)
        elif figure == 'N':
            nM = []
            gs.getKnightMoves(pos[0], pos[1] ,nM)
            return len(nM)
        elif figure == 'B':
            bM = []
            gs.getBishopMoves(pos[0], pos[1] ,bM)
            return len(bM)
        elif figure == 'R':
            rM= []
            gs.getRookMoves(pos[0], pos[1] ,rM)
            return len(rM)
        elif figure == 'K':
            kM = []
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

#------Move ordering functions------

    def check_winning_conditions(self,gs):
        """
        Check if the game is won

        Parameters
        ----------
        gs : GameState
            gamestate to be evaluated

        Returns
        -------
        bool

        """
        if gs.checkMate:
            return True
        else:
            return False

    def check_inCheck_condition(self,gs):
        """
        Check if the game is in check

        Parameters
        ----------
        gs : GameState
            gamestate to be evaluated

        Returns
        -------
        bool

        """
        if gs.inCheck:
            return True
        else:
            return False

    def check_is_capture_move(self,move):
        """
        Check if the move is a capture move

        Parameters
        ----------
        move : Move
            move to be evaluated

        Returns
        -------
        bool

        """
        if move.pieceCaptured != '--':
            return True
        else:
            return False

    def check_enemy_winning_conditions(self,gs):
        """
        Check if the enemy has won in th next move

        Parameters
        ----------
        gs : GameState
            gamestate to be evaluated

        Returns
        -------
        bool

        """
        nextValidMoves = gs.getValidMoves()

        for move in nextValidMoves:
            gs.makeMove(move)
            if gs.checkMate:
                return True
            else:
                gs.undoMove()
        return False

    def moveOrdering(self,gs,possibleMoves):
        """
        Order the moves descending from value

        Parameters
        ----------
        gs : GameState
            gamestate to be evaluated
        possibleMove : Move
            moves to be sorted

        Returns
        -------
        list: list of ordered moves

        """
        
        sorted_moves = []
        check_moves = []
        capture_moves = []
        last_moves =[]

        for move in possibleMoves:

            gs.makeMove(move)

            #check if the game is won
            if self.check_winning_conditions(gs):
                sorted_moves.insert(0,move)

            elif self.check_inCheck_condition(gs):
                check_moves.append(move)
            
            elif self.check_is_capture_move(move):
                capture_moves.append(move)

            elif self.check_enemy_winning_conditions(gs):
                last_moves.append(move)

            else:
                last_moves.insert(0,move)

            gs.undoMove()

        return (sorted_moves+check_moves+capture_moves+last_moves)
            








    


            
        

        
    
        

        

        