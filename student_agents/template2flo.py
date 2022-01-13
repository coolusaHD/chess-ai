import os
import random
import configparser
import time
# for analyzing processing time over all processes
from multiprocessing import Manager, Value

#
#   To create another agent:
#   cp this file into the new one
#   (optional:) Create a config file: [agentModuleName]Config.ini
#


class Agent:
    def __init__(self):
        # set the agent name to the Module's name (without the .py)
        self.agentName = "-- DEFAULT --"
        # move queue containing all moves the AI wants to take
        self.move_queue = None
        # save the piece color for this agent
        self.isWhite = None

        # analytics values
        # the number of nodes visited to find the move
        self.visitedNodes = 0
        # the number of times pruned to find the move
        self.timesPruned = 0
        # a list containing the times for all move calculations
        #ToDO: remove for final version
        manager = Manager()
        self.times = manager.list()
        self.nodes = manager.list()
        self.prunes = manager.list()
        self.moves = Value('i', 0)


        # weights determining the importance of material value and positional value for a move
        # to be chosen by the Agent
        # A higher positional value makes it think more about the attacking and attacked squares
        # while a higher material weight makes it trade more agressively
        self.positionalWeight = 1
        self.materialWeight = 10
        # the maximum recursion depth for alpha beta pruning. -1 if infinite depth should be used
        self.recursionDepth = 5
        # the value of each piece
        self.pieceWeights = {'p' : 1, 'N' : 3, 'B' : 4, 'R' : 5, 'K' : 1000}
        # a dictionary assigning values to the position of a piece depending on if its good or bad
        self.positionalWeights = {
        'wp' : [5, 5, 5, 5, 5, 5,
                5, 6, 7, 7, 6, 5,
                0, 0, 8, 8, 0, 0,
                0, 0, 7, 7, 0, 0,
                5, 6, -5, -5, 6,5,
                0, 0, 0, 0, 0, 0],

        'wN' : [-20, -15, -10, -10, -15, -20,
                -15, -10, 0, 0, -5, -5,
                -10, 0, 8, 8, 0, -5,
                -10, 0, 8, 8, 0, -5,
                -5, -4, 5, 5, -4, -5,
                -8, -4, -4, -4, -4, -8],

        'wB' :[-10, -5, -5, -5, -5, -10, -3, 0, 0, 0, 0, -3, -3, 0, 6, 6, 0, -3, -3, 6, 6, 6, 6, -3, -3, 5, 0, 0, 5, -3, -10, -5, -5, -5, -5, -10],

        'wR' : [0, 0, 0, 0, 0, 0,
                0, 10, 10, 10, 10, 0,
                0, 1, 1, 1, 1, 0,
                0, 1, 1, 1, 1, 0,
                0, 1, 1, 1, 1, 0,
                0, 0, 5, 5, 0, 0],

        'wK' : [-6, -6, -6, 6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -5, -6, -5, -6, -6, -6, -6, -5, 20, 20, 0, 0, 20, 20, 20, 25, 0, 0, 25, 20],

        'bp' : [0, 0, 0, 0, 0, 0,
                5, 6, -5, -5, 6, 5,
                0, 0, 7, 7, 0, 0,
                0, 0, 8, 8, 0, 0,
                5, 6, 7, 7, 6, 5,
                5, 5, 5, 5, 5, 5],

        'bN' : [-8, -4, -4, -4, -4, -8,
                -5, -4, 5, 5, -4, -5,
                -5, 0, 8, 8, 0, -10,
                -5, 0, 8, 8, 0, -10,
                -5, -5, 0, 0, -10, -15,
                -20, -15, -10, -10, -15, -20],

        'bB' : [-10, -5, -5, -5, -5, -10,
                -3, 5, 0, 0, 5, -3,
                -3, 6, 6, 6, 6, -3,
                -3, 0, 6, 6, 0, -3,
                -3, 0, 0, 0, 0, -3,
                -10, -5, -5, -5, -5, -10],

        'bR' : [0, 0, 5, 5, 0, 0,
                0, 1, 1, 1, 1, 0,
                0, 1, 1, 1, 1, 0,
                0, 1, 1, 1, 1, 0,
                0, 10, 10, 10, 10, 0,
                0, 0, 0, 0, 0, 0],

        'bK' : [20, 25, 0, 0, 25, 20,
                20, 20, 0, 0, 20, 20,
                -5, -6, -6, -6, -6, -5,
                -6, -5, -6, -6, -6, -6,
                -6, -6, -6, -6, -6, -6,
                -6, -6, 6, -6, -6, -6]}

    # function overriding the configuration values with the values from the given configuration file
    def ConfigFromFile(self, filePath):
        # override the values with ones from the agents config file if possible
        try:
            config = configparser.ConfigParser()
            config.read(filePath)
            self.pieceWeights = {
                'p' : int(config['WEIGHTS']['pawn']),
                'N' : int(config['WEIGHTS']['knight']),
                'B' : int(config['WEIGHTS']['bishop']),
                'R' : int(config['WEIGHTS']['rook']),
                'K' : int(config['WEIGHTS']['king'])}

            self.positionalWeight = int(config['WEIGHTS']['position'])
            self.materialWeight = int(config['WEIGHTS']['material'])
            self.recursionDepth = int(config['ALPHA_BETA_PRUNING']['depth'])
            self.agentName = filePath
            print("\nConfiguration from " + filePath + ":")
            print({section: dict(config[section]) for section in config.sections()})
            print()
        except:
            #
            #   could not open configuration file
            #

            warning = """\n █     █░ ▄▄▄       ██▀███   ███▄    █  ██▓ ███▄    █   ▄████
▓█░ █ ░█░▒████▄    ▓██ ▒ ██▒ ██ ▀█   █ ▓██▒ ██ ▀█   █  ██▒ ▀█▒
▒█░ █ ░█ ▒██  ▀█▄  ▓██ ░▄█ ▒▓██  ▀█ ██▒▒██▒▓██  ▀█ ██▒▒██░▄▄▄░
░█░ █ ░█ ░██▄▄▄▄██ ▒██▀▀█▄  ▓██▒  ▐▌██▒░██░▓██▒  ▐▌██▒░▓█  ██▓
░░██▒██▓  ▓█   ▓██▒░██▓ ▒██▒▒██░   ▓██░░██░▒██░   ▓██░░▒▓███▀▒
░ ▓░▒ ▒   ▒▒   ▓▒█░░ ▒▓ ░▒▓░░ ▒░   ▒ ▒ ░▓  ░ ▒░   ▒ ▒  ░▒   ▒
  ▒ ░ ░    ▒   ▒▒ ░  ░▒ ░ ▒░░ ░░   ░ ▒░ ▒ ░░ ░░   ░ ▒░  ░   ░
  ░   ░    ░   ▒     ░░   ░    ░   ░ ░  ▒ ░   ░   ░ ░ ░ ░   ░
    ░          ░  ░   ░              ░  ░           ░       ░ """
            print('-------------------------------------------------------------------')
            print(warning)
            print("\nNo Configuration file specified for Agent: " + filePath +  "\n\n")
            print('-------------------------------------------------------------------')


    # function returning the next move from the queue
    def get_move(self):
        move = None
        while not self.move_queue.empty():
            move = self.move_queue.get()
        return move

    # function adding a move to the queue
    def update_move(self, move, score, depth):
        """
        :param move: Object of class Move, like a list element of gamestate.getValidMoves()
        :param score: Integer; not really necessary, just for informative printing
        :param depth: Integer; not really necessary, just for informative printing
        :return:
        """
        self.move_queue.put([move, score, depth])
        #print("queued Move: " + str(move))

    def clear_queue(self, outer_queue):
        self.move_queue = outer_queue
        #print("Cleared Queue")

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
        none

        """
        # update the agent's color
        if(self.isWhite is None):
            self.isWhite = gs.whiteToMove

        self.moves.value += 1

        #print(self.ArrayToBoardSting(gs.board))

        startTime = time.time_ns()
        # use alpha beta pruning to determine the best move
        (bestMoveValue, bestMove) = self.AlphaBetaPruning(gs)

        # print performancy metrics
        delta = time.time_ns() - startTime
        self.times.append(delta)
        self.nodes.append(self.visitedNodes)
        self.prunes.append(self.timesPruned)

        print()
        print("Agent: " + self.agentName)
        print("Took %f s" % (delta / 1000000000))
        print("Visited: %d nodes, pruned %d times" %(self.visitedNodes, self.timesPruned))
        print("Times:         [Min: %f, Max: %f, Avg: %f]" %(min(self.times)/ 1000000000, max(self.times)/ 1000000000, self.Average(self.times)/ 1000000000))
        print("Nodes visited: [Min: %d, Max: %d, Avg: %d, All: %d]" %(min(self.nodes), max(self.nodes), self.Average(self.nodes), sum(self.nodes)))
        print("Times Pruned:  [Min: %d, Max: %d, Avg: %d]" %(min(self.prunes), max(self.prunes), self.Average(self.prunes)))
        print("Moves: %d, Nodes per Moves: %d" %(self.moves.value, sum(self.nodes) / self.moves.value))



        self.update_move(bestMove, bestMoveValue, 0)

        """
        print(self.ArrayToBoardSting(self.EvaluateState(gs)))
        # get all valid moves
        moves = gs.getValidMoves()
        # check if there is only one possible move
        if (len(moves) == 1):
            # select this move
            self.update_move(moves[0], 0, 0)
            return
        # go through all valid moves and find the best one
        bestMove = moves[0]
        bestMoveValue = self.EvaluateMove(gs, moves[0])

        for move in moves[1:]:
                moveValue = self.EvaluateMove(gs, move)
                if (moveValue > bestMoveValue):
                    bestMove = move
                    bestMoveValue = moveValue
        """

        #self.update_move(moves[0], 0, 0)


    # function evaluating the given move
    # @param gameState: the gameState
    # @param move: the Move to evaluate
    # @return: an integer value representing the value of the move
    def EvaluateMove(self, gameState, move):
        # calculate the positional and material value without the move
        valueBeforeMove = self.EvaluateState(gameState)

        # make the move
        gameState.makeMove(move)

        # calculate the positional and material value after the move
        valueAfterMove = self.EvaluateState(gameState)
        # return to the old state so the state does not get changed in total
        gameState.undoMove()
        # determine the value difference and return it
        return valueAfterMove - valueBeforeMove

    # function quickly estimating move evaluation
    # using only material evaluation and endstate evaluation
    # @param gameState: the game state before the move
    # @param move: the move to evaluate
    # @return: the approximate move value
    def EvaluateMoveQuick(self, gameState, move):
         # calculate the positional and material value without the move
        valueBeforeMove = self.GetMaterialValue(gameState.board) + self.EvaluateEndState(gameState)

        # make the move
        gameState.makeMove(move)

        # calculate the positional and material value after the move
        valueAfterMove = self.GetMaterialValue(gameState.board) + self.EvaluateEndState(gameState)
        # return to the old state so the state does not get changed in total
        gameState.undoMove()
        # determine the value difference and return it
        return valueAfterMove - valueBeforeMove


    # function evaluating the given state of the game
    # @param state: the game state to evaluate
    # @return: a list the size of the game field containing the 'goodness'-value of each square
    # Here, the goodness value represents the amount of friendly (positive) or enemy (negative)+
    # pieces attacking this square
    def EvaluateState(self, state):
        # calculate the positional value
        positionalValue = 0
        if(not self.positionalWeight == 0):
            positionalValue = self.GetPositionalValue(state) * self.positionalWeight
        # calculate the material value
        materialValue = self.GetMaterialValue(state.board) * self.materialWeight
        # calculate the end state value
        endStateValue = self.EvaluateEndState(state)
        # combine both to a final value
        return positionalValue + materialValue + endStateValue


    # function evaluating the end state if possible
    # @param state: the state to evaluate
    # @return: the end state value or 0 if the given state is no end state
    def EvaluateEndState(self, state):
        if (not state.checkMate):
            # the current state is no checkmate
            return 0
        # determine if the agent or enemy won
        if(state.whiteToMove):
            # black wins by checkmate
            if (self.isWhite):
                # agent lost
                return -100000
            # agent won
            return 100000
        else:
            # white wins by checkmate
            if (self.isWhite):
                # agent won
                return 100000
            # agent lost
            return -100000


    # function calculating how many pieces attack/defend a field for all fields
    # @param state: the game state to evaluate
    # @return: a list the size of the game field containing the positinal-value of each square
    def GetPositionalValue(self, state):
        #
        #       ToDo: The square on which the piece stands currently gets not evaluated???
        #       Determine if this is the wanted behavipur
        #       Maybe change evaluation to include current material of both players (myMaterial vs enemyMaterial)
        #
        # get the agent's team string
        teamColor = 'b'
        if (self.isWhite):
            teamColor = 'w'
        # initialize the positional value
        positionalValue = 0
        # go through all fields
        for position, piece in enumerate(state.board):
            # ignore empty fields
            if (piece == '--'):
                continue
            # add / subtract the positional value of the piece to the total value
            if(piece[0] == teamColor):
                positionalValue += self.positionalWeights[piece][position]
            else:
                positionalValue -= self.positionalWeights[piece][position]
        return positionalValue

    # function calculating all possible (legal) moves of the given piece
    # @param state: the gameState to get the moves for
    # @param row: the row of the piece to get the moves for
    # @param column: the column of the piece to get the moves for
    # @return (blackMoves, whiteMoves): the moves for each color
    def getMoves(self, state, row, column):
        # get the piece from the board
        piece = state.board[row * 6 + column]
        # save the currently playing  color
        # this needs to be done bc. state gets passed by reference
        whiteToMove = state.whiteToMove
        # determine the color of the given piece and set the state accordingly
        state.whiteToMove = (piece[0] == "w")
        # list for storing the valid moves
        moves = []
        # check for the type of piece and return its possible moves
        if (piece[1] == 'R'):
            # rook
            state.getRookMoves(row, column, moves)
        elif (piece[1] == 'B'):
            # bishop
            state.getBishopMoves(row, column, moves)
        elif (piece[1] == 'N'):
            # knight
            state.getKnightMoves(row, column, moves)
        elif (piece[1] == 'K'):
            # king
            state.getKingMoves(row, column, moves)
        elif (piece[1] == 'p'):
            # pawn
            state.getPawnMoves(row, column, moves)

        # restore the currently playing color
        state.whiteToMove = whiteToMove
        return moves



    # function returning the absolute material value on the board
    # using self.pieceWeights as weights by subtracting enemy material
    # from player material
    # @param board: a 36 element string array containing the state of the board
    #       to evaluate
    # @return: the absolute material value of the given board

    def GetMaterialValue(self, board):
        # get the agent's team string
        # ToDo: maybe do once and save it as agent variable
        teamColor = 'b'
        if (self.isWhite):
            teamColor = 'w'
        materialValue = 0
        # go through all pieces
        for piece in board:
            if (piece == '--'):
                # no piece on this square
                continue
            # check if the current piece is owned by the agent
            if(piece[0] == teamColor):
                # team color piece
                # add piece value to the material value
                materialValue += self.pieceWeights[piece[1]]
            else:
                # enemy color piece
                # subtract piece value from the material value
                materialValue -= self.pieceWeights[piece[1]]

        return materialValue


    # function summing up all values of the given list
    # @param list: a 1D-list of integer values
    # @return: the calculated sum or 0 if None was given
    def ListSum(self, intList):
        sum = 0
        for i in intList:
            sum += i
        return sum

    # function doing alpha-beta-pruning for the given game state
    # @param state: the game state to make alpha-beta-pruning for
    #       assumes that the player currently playing in the given state is the max player
    # @return: (bestValue, bestMove) for the current state and player
    def AlphaBetaPruning(self, state):
        #search for the best move in the current state
        # reset analytics values
        self.visitedNodes = 0
        self.timesPruned = 0

        # ToDo: change -100000 and 100000 to +-infinity or similar as this is only temporary
        return self.BestMove(state, -1000000, 1000000, self.recursionDepth)



    # function finding the best move of the current state using recursive alpha-beta pruning
    # @param state: the state to evaluate the moves for
    # @param alpha: the value of the best move found within previous searches
    # @param alpha: the value of the worst move found within previous searches
    # @param depth: the maximum recursion depth
    # @return: the best value and move found
    def BestMove(self, state, alpha, beta, depth):

        self.visitedNodes += 1
        # check if this state is a terminal state
        if (depth == 0 or state.checkMate or state.staleMate or state.threefold or state.draw):
            # an end state was reached
            # evaluate the end state
            #ToDo: differentiate between the different cases instead of evaluating the board
            # this is only temporary
            return (self.EvaluateState(state), None)

        # get all currently possible moves
        moves = state.getValidMoves()
        # sort the moves for better pruning
        self.SortMoves(state, moves)

        bestMoveValue = None
        bestMove = None
        # check if there are any more moves possible
        # ToDo: Check if this is necessary as this should be captured by the check above
        if (len(moves) == 0):
            return (self.EvaluateState(state), None)

        # go through all possible moves (backwards for better pruning when sorted)
        for move in reversed(moves):
            # get the min values of all possible moves
            state.makeMove(move)
            (value, nextMove) = self.WorstMove(state, alpha, beta, depth - 1)
            state.undoMove()


            # prune if the value is greater than beta as WorstMove won't choose a better one
            if (value >= beta):
                self.timesPruned += 1
                return (value, move)

            # update alpha value if needed
            if (value > alpha):
                alpha = value

            # find the best one out of all min value moves given
            if (bestMoveValue == None):
                bestMoveValue = value
                bestMove = move
            # check if the best move is better than the previous best move
            elif (value > bestMoveValue):
                # current move is better, replace old bestMove
                bestMoveValue = value
                bestMove = move

        return (bestMoveValue, bestMove)




    # function finding the worst move of the current state using recursive alpha-beta pruning
    # @param state: the state to evaluate the moves for
    # @param alpha: the value of the best move found within previous searches
    # @param alpha: the value of the worst move found within previous searches
    # @param depth: the maximum recursion depth
    # @return: the worst value and move found
    def WorstMove(self, state, alpha, beta, depth):
        self.visitedNodes += 1
        # check if this state is a terminal state
        if (depth == 0 or state.checkMate or state.staleMate or state.threefold or state.draw):
            # an end state was reached
            # evaluate the end state
            #ToDo: differentiate between the different cases instead of evaluating the board
            # this is only temporary
            return (self.EvaluateState(state), None)

        # get all currently possible moves
        moves = state.getValidMoves()
        # sort the moves for better pruning
        self.SortMoves(state, moves)

        worstMoveValue = None
        worstMove = None

        # check if there are any more moves possible
        # ToDo: Check if this is necessary as this should be captured by the check above
        if (len(moves) == 0):
            return (self.EvaluateState(state), None)

        # go through all possible moves
        for move in moves:
            # get the min values of all possible moves
            state.makeMove(move)
            (value, nextMove) = self.BestMove(state, alpha, beta, depth -1)
            state.undoMove()
            # prune if the value is less than alpha as BestMove won't choose a worse value
            if (value <= alpha):
                self.timesPruned += 1
                return (value, move)

            # update beta if needed
            if (value < beta):
                beta = value
            # find the worst one out of all max value moves given
            if (worstMoveValue == None):
                worstMoveValue = value
                worstMove = move
            # check if the current move is worse than the previous worst move
            elif (value < worstMoveValue):
                # current move is worse, replace old wostMove
                worstMoveValue = value
                worstMove = move

        return (worstMoveValue, worstMove)

    # print the given array in the board's format
    def ArrayToBoardSting(self, array):
        result = []
        for i in range(len(array)):
            if (i % 6 == 0):
                result.append('\n\n\n\n')
            result.append(str(array[i]))
            result.append(" "* (4 - len(str(array[i]))))
        return " ".join(i for i in result)

    # function calculating the average of the given list
    def Average(self, list):
        return sum(list) / len(list)

    # function sorting the given list by a special heuristic for alpha beta pruning
    # @param state: the current game state
    # @param list: the moves to sort; in place, therefore no return value is needed
    def SortMoves(self, state, moves):
        sorted(moves, key=lambda m: self.EvaluateMoveQuick(state, m))
