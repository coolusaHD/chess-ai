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
            #print('Table counter: ', self.tableCounter)

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
        if string == 'bp':
            return 0
        elif string == 'bN':
            return 1
        elif string == 'bB':
            return 2
        elif string == 'bR':
            return 3
        elif string == 'bK':
            return 4
        elif string == 'wp':
            return 5
        elif string == 'wN':
            return 6
        elif string == 'wB':
            return 7
        elif string == 'wR':
            return 8
        elif string == 'wK':
            return 9
        else:
            return -1
        
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
        if num == 0:
            return 'bp'
        elif num == 1:
            return 'bN'
        elif num == 2:
            return 'bB'
        elif num == 3:
            return 'bR'
        elif num == 4:
            return 'bK'
        elif num == 5:
            return 'wp'
        elif num == 6:
            return 'wN'
        elif num == 7:
            return 'wB'
        elif num == 8:
            return 'wR'
        elif num == 9:
            return 'wK'
        else:
            return None

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
            for j in range(10):
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
                if gs.board[i] != '--':
                    hash ^= self.zobristTable[i][self.indciesOfFigures(gs.board[i])]
        return hash

    def updatezTableFromMove(self, gs, move):
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
        None

        """
        #update zobrist table from start and end position of move
        startPos = move.startRC
        endPos = move.endRC
        figure = move.pieceMoved
        self.hashedBoard ^= self.zobristTable[startPos][self.indciesOfFigures('--')]
        self.hashedBoard ^= self.zobristTable[endPos][self.indciesOfFigures(figure)]

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
        
            
        #    #check if evaluated gamestate is in table
        #    #hash actual board
        #    actualBoardHashed = self.hashBoard(gs)
        #    
        #    #get item from table
        #    maybeSavedEntry = self.hashStorageTable.get(actualBoardHashed)
#
        #    if maybeSavedEntry != None:# and (maybeSavedEntry['player'] == maxPlayer): and maybeSavedEntry['depth'] == depth:
        #        #print('returning from table')
        #        #self.tableCounter += 1
        #        return maybeSavedEntry['score']
        #    else:
        #        return self.Quiesce(gs, alpha, beta)



        #get all valid moves
        validMoves = gs.getValidMoves()

          #check for timeout
        if datetime.datetime.now() > self.timeout:
            return None
         #check for endgame
        if depth == 0 or gs.checkMate or gs.staleMate or gs.threefold or gs.draw:
            return self.evaluateBoard(gs)

        #check for maxPlayer
        if maxPlayer:

         
            #move ordering for maxPlayer
            #validMoves = self.moveOrdering(validMoves, gs, maxPlayer)

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

                #save score of gamestate in table
                #self.hashStorageTable[self.hashBoard(copyGS)] = {'score': score, 'depth': depth, 'player': maxPlayer}

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
            #validMoves = self.moveOrdering(validMoves, gs, maxPlayer)

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

                #save score of gamestate in table
                #self.hashStorageTable[self.hashBoard(copyGS)] = {'score': score, 'depth': depth, 'player': maxPlayer}

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

    def Quiesce(self, gs, alpha, beta):
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

        stand_pat = self.evaluateBoard(gs)
        if(stand_pat >= beta):
            return beta
        if(alpha < stand_pat):
            alpha = stand_pat
        #consider every capture
        validMoves = gs.getValidMoves()
        for move in validMoves:
            if move.isCapture:
                gs.makeMove(move)
                score = -self.Quiesce(gs, -beta, -alpha)
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

    def moveOrdering(self, moves, gs, maxPlayer):
        """
        Helper method to order moves based on their evaluation

        Parameters
        ----------
        moves : Moves
            list of moves to be ordered
        gs : GameState
            current game state
        maxPlayer : bool
            true if max iteration, false if min iteration

        Returns
        -------
        orderedMoves : Moves
            list of ordered moves

        """
        orderedMoves = []
        for move in moves:
            gs.makeMove(move)

            #check if evaluated gamestate is in table
            #hash actual board
            actualBoardHashed = self.hashBoard(gs)
            
            #get item from table
            maybeSavedEntry = self.hashStorageTable.get(actualBoardHashed)

            if maybeSavedEntry != None:
                score = maybeSavedEntry['score']
            else:
                score = self.evaluateBoard(gs)

            gs.undoMove()
            orderedMoves.append((score, move))

        #sort moves by highest score
        orderedMoves.sort(key=lambda x: x[0], reverse = maxPlayer)

        # #split list into two lists
        # orderedMoves1 = orderedMoves[:len(orderedMoves)//2]
        # orderedMoves2 = orderedMoves[len(orderedMoves)//2:]
        # #reverse second list
        # orderedMoves2 = orderedMoves2[::-1]
        # #append both lists
        # orderedMoves = orderedMoves1 + orderedMoves2

        #return only moves
        return [move for score, move in orderedMoves]

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










    


            
        

        
    
        

        

        