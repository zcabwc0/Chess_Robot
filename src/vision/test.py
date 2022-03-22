import chess
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
def check_num(color):
    color = np.array(color)
    if(len(color[color == chess.WHITE]) ==16 and
        len(color[color == chess.BLACK]) ==16 and
        len(color[color == None]) == 32):
        print('Number of pieces correct!')
    else:
        print('Wrong pieces number!!!')
def load_pca_svc():
    path = "./data/squares/color"
    with open(os.path.join(path, "color_detection.pca"), 'rb') as pca_file:
        pca = pickle.load(pca_file)
    with open(os.path.join(path, "color_detection.svc"), 'rb') as svc_file:
        svc = pickle.load(svc_file)
    return pca, svc


vid = cv2.VideoCapture(0)
ret, frame = vid.read()
frame = cv2.warpPerspective(frame, perspectiveM,(480,480))
cv2.imwrite('test.jpg',frame)
new_board = Chessboard(frame)
board = chess.BaseBoard()
pca, svc = load_pca_svc()
checker = board_checker(board, new_board, pca, svc)
new_color = checker.detect_new_color()
show_color(new_color)
check_num(new_color)