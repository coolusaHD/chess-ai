
import random
import numpy as np

class Agent:
    def __init__(self):
        self.move_queue = None
        self.points = {
            '--' : 0,
            'bR' : -5,
            'bB' : -3,
            'bN' : -3,
            'bK' : -90,
            'bp' : -1,
            'wR' : 5,
            'wB' : 3,
            'wN' : 3,
            'wK' : 90,
            'wp' : 1,
        }
        self.adv_points = {
            '--' : np.zeros((6,6)),
            'wp' : np.array([
                [0,  0,     0,  0,      0,  0],
                [30, 35,    40, 40,    35, 30],
                [5,  7.5,   25, 25,    7.5,  5],
                [0,  0,     20, 20,    0,  0],
                [5, 2.5,   -10,  -10,     2.5,  5],
                [0,  0,     0,  0,     0,  0]]),
            'wN' : np.array([
                [-50,-35,-30,-30, -35, -50],
                [-35,-7.5,  7.5,  7.5, -7.5,-35],
                [-30,  10, 20, 20, 10,-30],
                [-30,  7.5, 20, 20, 7.5,-30],
                [-35,-2,  10,  10,-2,-35],
                [-50,-35,-30,-30,-35,-50]]),
            'wB' : np.array([
                [-20,-10,-10,-10,-10,-20],
                [-10,  1.25,  5,  5,  2.15,-10],
                [-10,  5, 10, 10,  5,-10],
                [-10,  5, 10, 10,  5,-10],
                [-10,  6.25,  5,  5,  6.125,-10],
                [-20,-10,-10,-10,-10,-20]]),
            'wR' : np.array([
                [0,  0,  0,  0,  0, 0],
                [0,  5,  5,  5,  5, 0],
                [-5,  0,  0,  0,  0, -5],
                [-5,  0,  0,  0,  0, -5],
                [-5,  0,  0,  0,  0, -5],
                [0,  0,  5,  5,  0,  0]]),
            'wK' : np.array([
                [-30,-40,-50,-50,-40,-30],
                [-30,-40,-50,-50,-40,-30],
                [-30,-40,-50,-50,-40,-30],
                [-20,-30,-40,-40,-30,-20],
                [10, -5,  -10,  -10, -5, 10],
                [20, 20,  0,  0, 20, 20]])}
        self.adv_points['bp'] = np.flipud(self.adv_points['wp']*(-1))
        self.adv_points['bN'] = np.flipud(self.adv_points['wN']*(-1))
        self.adv_points['bB'] = np.flipud(self.adv_points['wB']*(-1))
        self.adv_points['bR'] = np.flipud(self.adv_points['wR']*(-1))
        self.adv_points['bK'] = np.flipud(self.adv_points['wK']*(-1))


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

    def evaluate(self, gs):
        score = 0
        #position = 0
        #for field in gs.board:
        #    score += self.points[field]
        #    score += self.adv_points[field][position//6][position%6]/100
        #    position += 1
        score = np.sum([self.points[figure] for figure in gs.board])
        return score

    def findBestMove(self, gs):
        depth = 5

        if gs.whiteToMove:
            next_move, best_score = self.maxSearch(gs, -10000, 10000, depth)
        else:
            next_move, best_score = self.minSearch(gs, -10000, 10000, depth)
        self.update_move(next_move, -1, -1)

    
    def maxSearch(self, gs, alpha, beta, depth): 
        best_move = None  
        best_score = -10000
        if depth == 0: return [None, self.evaluate(gs)] 
        if gs.checkMate: return [None, best_score]
        if gs.staleMate: return [None, 0]
        

        for move in gs.getValidMoves():
            gs.makeMove(move)
            next_move, min_next_score = self.minSearch(gs, alpha, beta, depth-1)
            gs.undoMove()

            if min_next_score > best_score:
                best_score = min_next_score
                best_move = move
        
            if best_score >= beta: return move, best_score
            alpha = np.max([alpha, best_score])      
        return best_move, best_score

    def minSearch(self, gs, alpha, beta, depth):
        best_move = None
        best_score = 10000
        if depth == 0: return [None, self.evaluate(gs)] 
        if gs.checkMate: return [None, best_score]
        if gs.staleMate: return [None, 0]
        

        for move in gs.getValidMoves():
            gs.makeMove(move)
            next_move, max_next_score= self.maxSearch(gs, alpha, beta, depth-1)
            gs.undoMove()

            if max_next_score < best_score:
                best_score = max_next_score
                best_move = move
        
            if best_score <= alpha: return move, best_score
            beta = np.min([beta, best_score])      
        return best_move, best_score