import chess
from chess import uci
from stockfish import Stockfish
import cv2
from .state_check import board_checker
import pickle
import os
from .chessboard import Chessboard
import numpy as np

perspectiveM = np.load('perspectiveMatrix.npy')
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

vid = cv2.VideoCapture(0)
engine = uci.popen_engine('stockfish')
init_fen = chess.STARTING_FEN
fen_path = "current_game.fen"
with open(fen_path, 'w') as f:
    f.write(init_fen)
current_fen = ''


with open(fen_path, 'r') as f:
    current_fen = f.read()
board = chess.Board(current_fen)
print(board.legal_moves)
while(True):
    ret, frame = vid.read()
    frame = cv2.warpPerspective(frame, perspectiveM,(480,480))
    cv2.imshow('frame',frame)
    press = cv2.waitKey(1) & 0xFF
    if press == ord('q'): #quit
        break
cv2.destroyAllWindows()

new_board = Chessboard(frame)
pca, svc = load_pca_svc()
checker = board_checker(board, new_board,pca,svc)
replace, current_move = checker.check()
print(replace, current_move)
if(not check_move(board,current_move)):
    print("Illegal move, please redone your move!!")
    assert 0
board.push(chess.Move.from_uci(current_move))
best_move = get_best_move(engine, board)
board.push(best_move)
with open(fen_path, 'w') as f:
    f.write(board.fen())
print(best_move)


