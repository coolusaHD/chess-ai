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
        self.timeout = self.start + 1900000

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
    kingSingleEval = 500


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
            return self.evaluateBlack(gs)-self.evaluateWhite(gs)
        else:
            return self.evaluateWhite(gs)-self.evaluateBlack(gs)
    

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
                break
            if self.getBoardFigure(gs, i) == 'bN':
                score += self.knightSingleEval + self.knightEvalBlack[i]
                break
            if self.getBoardFigure(gs, i) == 'bB':
                score += self.bishopSingleEval + self.bishopEvalBlack[i]
                break
            if self.getBoardFigure(gs, i) == 'bR':
                score += self.rookSingleEval + self.rookEvalBlack[i]
                break
            if self.getBoardFigure(gs, i) == 'bK':
                score += self.kingSingleEval + self.kingEvalBlack[i]
                break
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


    def evaluateBoard(self, gs):
        """
        Evaluate the gamestate for the board 
        score is the sum of the categories when calc evaluate White - evaluate Black
        to get evaluation for black, multiply by -1

        Parameters
        ----------
        gs : GameState
            gamestate to be evaluated

        Returns
        -------
        float

        """
        score = 0
        
        #check for king safety
        score += self.evalKingSafety(gs)
        
        #check material
        score += self.evalMaterial(gs)

        #check for pieces activity
        score += self.evalPiecesActivity(gs)

        #check for pawns structure
        score += self.evalPawnsStructure(gs)
        

        return score


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
        score = 0

        #get position of black king
        listbK = self.getPositionOfFigure(gs, 'bK')
        listwK = self.getPositionOfFigure(gs, 'wK')

        colwK = listwK[0][0]
        rowwK = listwK[0][1]

        colbK = listbK[0][0]
        rowbK = listbK[0][1]

        
        #check for king safety
        #if the own king is safe -> +1 if not -2
        #if the enemy king is safe -> -1 if not +2
        if gs.whiteToMove :
            #white to move
            # check enemy king 
            if gs.squareUnderAttack(rowbK, colbK):
                score += 2*self.pawnSingleEval
            else:
                score -= self.pawnSingleEval/2
            #check own king
            if gs.squareUnderAttack(rowwK, colwK):
                score -= self.pawnSingleEval
            else:
                score += 2*self.pawnSingleEval

        else:
            #black to move 
            # check enemy king
            if gs.squareUnderAttack(rowwK, colwK):
                score += 2*self.pawnSingleEval
            else:
                score -= self.pawnSingleEval/2
            #check own king
            if gs.squareUnderAttack(rowbK, colbK):
                score -= self.pawnSingleEval
            else:
                score += 2*self.pawnSingleEval
            
        return score

    def getPositionOfFigure(gs, figure):
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
        list with tupels
            int, col of figure
            int, row of figure

        """
        list = []
        for i in range(0, 35):
            if gs.board[i] == figure:
                # row = i // 6  -> divide by 6 without remainder
                # col = i % 6  -> modulo 6
                list.append((i // 6, i % 6))

        return list

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
        scoreW = 0
        scoreB = 0
        #calculate material for white and black
        for i in range(0, 35):
            if gs.board[i] == 'bp':
                scoreB += self.pawnSingleEval
            elif gs.board[i] == 'bN':
                scoreB += self.knightSingleEval
            elif gs.board[i] == 'bB':
                scoreB += self.bishopSingleEval
            elif gs.board[i] == 'bR':
                scoreB += self.rookSingleEval
            elif gs.board[i] == 'bK':
                scoreB += self.kingSingleEval
            elif gs.board[i] == 'wp':
                scoreW -= self.pawnSingleEval
            elif gs.board[i] == 'wN':
                scoreW -= self.knightSingleEval
            elif gs.board[i] == 'wB':
                scoreW -= self.bishopSingleEval
            elif gs.board[i] == 'wR':
                scoreW -= self.rookSingleEval
            elif gs.board[i] == 'wK':
                scoreW -= self.kingSingleEval

        #return difference of material
        return scoreW-scoreB

    def evalPiecesActivity(self, gs):
        """
        Evaluate the pieces activity

        Parameters
        ----------
        gs : GameState
            gamestate to be evaluated

        Returns
        -------
        int

        """
        score = 0
        #check for pawn activity
        score += self.evalPawnActivity(gs)
        #check for knight activity
        score += self.evalKnightActivity(gs)
        #check for bishop activity
        score += self.evalBishopActivity(gs)
        #check for rook activity
        score += self.evalRookActivity(gs)

        return score

    def evalPawnActivity(self, gs):
        """
        Evaluate the pawn activity

        Parameters
        ----------
        gs : GameState
            gamestate to be evaluated

        Returns
        -------
        int: score

        """
        score = 0
        #check for pawn activity

        #get position of white pawns
        if gs.whiteToMove:
            listOfPawnPos = self.getPositionOfFigure(gs, 'wP')
        else:
            listOfPawnPos = self.getPositionOfFigure(gs, 'bP')
        #check if any pawn can be attacked by any enemy
        for pawnPos in listOfPawnPos:
            if gs.squareUnderAttack(pawnPos[1], pawnPos[0]):
                score -= self.pawnSingleEval/5

    def evalKnightActivity(self,gs):
        """
        Evaluate the knight activity

        Parameters
        ----------
        gs : GameState
            gamestate to be evaluated

        Returns
        -------
        int: score

        """
        score = 0
        #check for knight activity
        #get position of white knights
        if gs.whiteToMove:
            listOfKnightPos = self.getPositionOfFigure(gs, 'wN')
        else:
            listOfKnightPos = self.getPositionOfFigure(gs, 'bN')
        #check if any knight can be attacked by any enemy
        for knightPos in listOfKnightPos:
            if gs.squareUnderAttack(knightPos[1], knightPos[0]):
                score -= self.knightSingleEval/4

        return score

    def evalBishopActivity(self, gs):
        """
        Evaluate the bishop activity

        Parameters
        ----------
        gs : GameState
            gamestate to be evaluated

        Returns
        -------
        int: score

        """
        score = 0
        #check for bishop activity
        #get position of white bishops
        if gs.whiteToMove:
            listOfBishopPos = self.getPositionOfFigure(gs, 'wB')
        else:
            listOfBishopPos = self.getPositionOfFigure(gs, 'bB')
        #check if any bishop can be attacked by any enemy
        for bishopPos in listOfBishopPos:
            if gs.squareUnderAttack(bishopPos[1], bishopPos[0]):
                score -= self.bishopSingleEval/3

        return score

    def evalRookActivity(self, gs):
        """
        Evaluate the rook activity

        Parameters
        ----------
        gs : GameState
            gamestate to be evaluated

        Returns
        -------
        int: score

        """
        score = 0
        #check for rook activity
        #get position of white rooks
        if gs.whiteToMove:
            listOfRookPos = self.getPositionOfFigure(gs, 'wR')
        else:
            listOfRookPos = self.getPositionOfFigure(gs, 'bR')
        #check if any rook can be attacked by any enemy
        for rookPos in listOfRookPos:
            if gs.squareUnderAttack(rookPos[1], rookPos[0]):
                score -= self.rookSingleEval/2

        return score

    def evalKingActivity(self, gs):
        """
        Evaluate the king activity

        Parameters
        ----------
        gs : GameState
            gamestate to be evaluated

        Returns
        -------
        int: score

        """
        score = 0
        #check for king activity
        #get position of white king
        if gs.whiteToMove:
            listOfKingPos = self.getPositionOfFigure(gs, 'wK')
        else:
            listOfKingPos = self.getPositionOfFigure(gs, 'bK')
        #check if any king can be attacked by any enemy
        for kingPos in listOfKingPos:
            if gs.squareUnderAttack(kingPos[1], kingPos[0]):
                score -= self.kingSingleEval

        return score

    def evalPawnsStructure(self, gs):
        """
        Evaluate the pawn structure

        Parameters
        ----------
        gs : GameState
            gamestate to be evaluated

        Returns
        -------
        int: score

        """
        scoreW = 0
        scoreB = 0
        #check for pawn structure
        #get position of white pawns
        if gs.whiteToMove:
            listOfPawnPos = self.getPositionOfFigure(gs, 'wP')

            #check isolated pawns
            #->if there is no pawn diagonal behind, it is a backward pawn
            for pawnPos in listOfPawnPos:
                if pawnPos[0]==6:
                    scoreW += self.pawnSingleEval/6
                elif pawnPos[0] >= 5:
                    digonalLeftPos = (pawnPos[0]+1, pawnPos[1]-1)
                    digonalRightPos = (pawnPos[0]+1, pawnPos[1]+1)
                    diagonalLeftPosIndex = self.getIndexOfPosition(gs, digonalLeftPos)
                    diagonalRightPosIndex = self.getIndexOfPosition(gs, digonalRightPos)

                    if not (gs.board[diagonalLeftPosIndex] == 'wp' or gs.board[diagonalRightPosIndex] == 'wp'):
                        scoreW -= self.pawnSingleEval/3
                    
                
            #check pawn chain
            #->if there is are multiple pawns in a diagonal, it is a pawn chain
            for pawnPos in listOfPawnPos:
                if pawnPos[0] != 0:
                    digonalLeft1Pos = (pawnPos[0]+1, pawnPos[1]-1)
                    digonalLeft2Pos = (pawnPos[0]+2, pawnPos[1]-2)
                    digonalRight1Pos = (pawnPos[0]+1, pawnPos[1]+1)
                    digonalRight2Pos = (pawnPos[0]+2, pawnPos[1]+2)
                    diagonalLeft1PosIndex = self.getIndexOfPosition(gs, digonalLeft1Pos)
                    diagonalLeft2PosIndex = self.getIndexOfPosition(gs, digonalLeft2Pos)
                    diagonalRight1PosIndex = self.getIndexOfPosition(gs, digonalRight1Pos)
                    diagonalRight2PosIndex = self.getIndexOfPosition(gs, digonalRight2Pos)

                    #check for right diagonal chain
                    if gs.board[diagonalLeft1PosIndex] == 'wp' and gs.board[diagonalLeft2PosIndex] == 'wp':
                        scoreW += self.pawnSingleEval/4
                    #check for left diagonal chain
                    if gs.board[diagonalRight1PosIndex] == 'wp' and gs.board[diagonalRight2PosIndex] == 'wp':
                        scoreW += self.pawnSingleEval/4
                    
                    #check for double pawn chain
                    if gs.board[diagonalLeft1PosIndex] == 'wp' or  gs.board[diagonalRight1PosIndex] == 'wp':
                        scoreW += self.pawnSingleEval/4

                    #check for spike chain
                    if gs.board[diagonalLeft1PosIndex] == 'wp' and gs.board[diagonalRight1PosIndex] == 'wp':
                        scoreW += self.pawnSingleEval/2



        else: #black pawns
            listOfPawnPos = self.getPositionOfFigure(gs, 'bP')
        
            #check isolated pawns
            #->if there is no pawn diagonal behind, it is a backward pawn
            for pawnPos in listOfPawnPos:
                if pawnPos[0]==0:
                    scoreB += self.pawnSingleEval/6
                elif pawnPos[0] >= 2:
                    digonalLeftPos = (pawnPos[0]-1, pawnPos[1]-1)
                    digonalRightPos = (pawnPos[0]-1, pawnPos[1]+1)
                    diagonalLeftPosIndex = self.getIndexOfPosition(gs, digonalLeftPos)
                    diagonalRightPosIndex = self.getIndexOfPosition(gs, digonalRightPos)

                    if not (gs.board[diagonalLeftPosIndex] == 'wp' or gs.board[diagonalRightPosIndex] == 'wp'):
                        scoreB -= self.pawnSingleEval/3
                    
                
            #check pawn chain
            #->if there is are multiple pawns in a diagonal, it is a pawn chain
            for pawnPos in listOfPawnPos:
                if pawnPos[0] != 0:
                    digonalLeft1Pos = (pawnPos[0]-1, pawnPos[1]-1)
                    digonalLeft2Pos = (pawnPos[0]-2, pawnPos[1]-2)
                    digonalRight1Pos = (pawnPos[0]-1, pawnPos[1]+1)
                    digonalRight2Pos = (pawnPos[0]-2, pawnPos[1]+2)
                    diagonalLeft1PosIndex = self.getIndexOfPosition(gs, digonalLeft1Pos)
                    diagonalLeft2PosIndex = self.getIndexOfPosition(gs, digonalLeft2Pos)
                    diagonalRight1PosIndex = self.getIndexOfPosition(gs, digonalRight1Pos)
                    diagonalRight2PosIndex = self.getIndexOfPosition(gs, digonalRight2Pos)

                    #check for right diagonal chain
                    if gs.board[diagonalLeft1PosIndex] == 'wp' and gs.board[diagonalLeft2PosIndex] == 'wp':
                        scoreB += self.pawnSingleEval/4
                    #check for left diagonal chain
                    if gs.board[diagonalRight1PosIndex] == 'wp' and gs.board[diagonalRight2PosIndex] == 'wp':
                        scoreB += self.pawnSingleEval/4
                    
                    #check for double pawn chain
                    if gs.board[diagonalLeft1PosIndex] == 'wp' or  gs.board[diagonalRight1PosIndex] == 'wp':
                        scoreB += self.pawnSingleEval/4

                    #check for spike chain
                    if gs.board[diagonalLeft1PosIndex] == 'wp' and gs.board[diagonalRight1PosIndex] == 'wp':
                        scoreB += self.pawnSingleEval/2


        #calculate score
        score = scoreW - scoreB

        return score


    def getIndexOfPosition(gs, posList):
        """
        Get the index of a position in the board

        Parameters
        ----------
        gs : GameState
            gamestate to be evaluated
        posList : list
            list of position

        Returns
        -------
        int: index

        """
        index = 0
        #add col
        index += posList[1]*6
        #add row
        index += posList[0]
        return index
    


            
        

        
    
        

        

        