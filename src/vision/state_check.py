import chess
import numpy as np
from .constant import WHITE_PIECES, BLACK_PIECES, INDEX_TO_POSITION

class board_checker():
    def __init__(self, init_board, new_board, pca, svm): #init_board type is the board state in chess library, new_board type is class Chessboard
        self.init_board = init_board
        self.new_board = new_board
        self.pca = pca
        self.svm = svm
    
    def check_difference(self,init_color, new_color):
        origin_p = 0
        new_p = 0
        for i in range(64):
            if(init_color[i] != new_color[i]):
                if(init_color[i] == None):
                    new_p = i
                elif(new_color[i] == None):
                    origin_p = i
                else:
                    new_p = i
        current_move = INDEX_TO_POSITION[origin_p] + INDEX_TO_POSITION[new_p]
        return current_move
    
    def detect_new_color(self):
        color = []
        for i in range(64):
            sq = self.new_board.square_at(i)
            features = sq.img.flatten()
            X = features.reshape(1,-1).astype(np.float32)
            after_pca = self.pca.transform(X)
            pred = self.svm.predict(after_pca)[0]
            if pred == 1:
                color.append(chess.BLACK)
            elif pred == 2:
                color.append(chess.WHITE)
            else:
                color.append(None)
        return color
    
    def detect_init_color(self):
        color = []
        board = self.init_board
        for i in range(64):
            piece_type = board.piece_at(i)
            if piece_type in BLACK_PIECES:
                color.append(chess.BLACK)
            elif piece_type in WHITE_PIECES:
                color.append(chess.WHITE)
            else:
                color.append(None)
        return color

    def check(self):
        init_color = self.detect_init_color()
        new_color = self.detect_new_color()
        return self.check_difference(init_color,new_color)