import chess
import random
import numpy as np
import cv2
import os

class random_board:
    def __init__(self, p_number = 8, P_number = 8, n_number = 2, N_number = 2, b_number = 2, B_number = 2,
    r_number = 2, R_number = 2, k_number = 1, K_number = 1, q_number = 1, Q_number = 1, none_number = 32, index = 0):
        self.index = index
        self.pieces = []
        self.pieces += [chess.Piece(chess.PAWN, chess.BLACK)] * p_number
        self.pieces += [chess.Piece(chess.PAWN, chess.WHITE)] * P_number
        self.pieces += [chess.Piece(chess.KNIGHT, chess.BLACK)] * n_number
        self.pieces += [chess.Piece(chess.KNIGHT, chess.WHITE)] * N_number
        self.pieces += [chess.Piece(chess.BISHOP, chess.BLACK)] * b_number
        self.pieces += [chess.Piece(chess.BISHOP, chess.WHITE)] * B_number
        self.pieces += [chess.Piece(chess.ROOK, chess.BLACK)] * r_number
        self.pieces += [chess.Piece(chess.ROOK, chess.WHITE)] * R_number
        self.pieces += [chess.Piece(chess.KING, chess.BLACK)] * k_number
        self.pieces += [chess.Piece(chess.KING, chess.WHITE)] * K_number
        self.pieces += [chess.Piece(chess.QUEEN, chess.BLACK)] * q_number
        self.pieces += [chess.Piece(chess.QUEEN, chess.WHITE)] * Q_number
        self.pieces += [None] * none_number
        random.shuffle(self.pieces)
    
    def board(self):
        board = chess.BaseBoard.empty()
        for i in range(64):
            board.set_piece_at(i,self.pieces[i])
        return board
    
    def fen(self):
        return self.board().board_fen()
    
    def __str__(self):
        return str(self.board())

def create_folder(data_path, board):
    dir_path = os.path.join(data_path, str(board.index))
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    fen_path = os.path.join(data_path,str(board.index),"board.fen")
    if not os.path.exists(fen_path):
        with open(fen_path, 'w') as f:
            print(board.fen())
            f.write(board.fen())
    return dir_path

data_path = "./data/raw_image"
index = input('enter index of current data: ')
image_index = 0
vid = cv2.VideoCapture(0)

perspectiveM = np.load('perspectiveMatrix.npy')

board_gen = random_board(index = index)
print(board_gen.board())
while(True):
    ret, frame = vid.read()
    frame = cv2.warpPerspective(frame, perspectiveM,(480,480))
    cv2.imshow('frame',frame)
    press = cv2.waitKey(1) & 0xFF
    if press == ord('s'): #save image
        dir_path = create_folder(data_path, board_gen)
        fn = '_'.join(['board', str(image_index)]) + '.jpg'
        cv2.imwrite(os.path.join(dir_path, fn), frame)
        print('Success! Image ' + str(image_index))
        image_index += 1
    if press == ord('q'): #quit
        break

cv2.destroyAllWindows()