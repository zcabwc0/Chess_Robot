import chess
from chess import uci
import cv2
from .state_check import board_checker
import pickle
import os
from .chessboard import Chessboard
import numpy as np
from .constant import INDEX_TO_POSITION

def show_color(color):
    color = np.array(color).reshape(8,8)
    for x in range(8):
        print(color[7-x])

def check_move(board, move):
    legal_moves = board.legal_moves
    return chess.Move.from_uci(move) in legal_moves

def load_pca_svc():
    path = "./data/squares/color"
    with open(os.path.join(path, "color_detection.pca"), 'rb') as pca_file:
        pca = pickle.load(pca_file)
    with open(os.path.join(path, "color_detection.svc"), 'rb') as svc_file:
        svc = pickle.load(svc_file)
    return pca, svc

def get_best_move(engine, board):
    engine.position(board)
    result = engine.go(movetime=1000)
    return result.bestmove

def check_replace(board, move):
    replace = False
    des_position = INDEX_TO_POSITION.index(str(move)[2:4])
    if(board.piece_at(des_position) is not None):
        replace = True
    return replace

# Load camera capture and chess engine
vid = cv2.VideoCapture(0)
engine = uci.popen_engine('stockfish')
current_fen = ''
fen_path = "current_game.fen"
perspectiveM = np.load('perspectiveMatrix.npy')
print("Iteration: " + str(iter))
with open(fen_path, 'r') as f:
    current_fen = f.read()
board = chess.Board(current_fen)
# For test, suggest human the best move
# Wait for human's move, noticed by press 'q'
while(True):
    ret, frame = vid.read()
    frame = cv2.warpPerspective(frame, perspectiveM,(480,480))
    cv2.imshow('frame',frame)
    press = cv2.waitKey(1) & 0xFF
    if press == ord('q'): #quit
        break
cv2.destroyAllWindows()
cv2.imwrite("Board_Color.jpg", frame)
# Detect the human player's move using PCA and SVM
new_board = Chessboard(frame)
pca, svc = load_pca_svc()
checker = board_checker(board, new_board,pca,svc)
current_move = checker.check()
color = checker.detect_new_color()
show_color(color)