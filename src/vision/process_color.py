import os
import chess
import cv2
from constant import BOARD_SIZE,SQUARE_SIZE, WHITE_PIECES, BLACK_PIECES
from chessboard import Chessboard
from square import Square
import numpy as np
import datetime

def create_dir(des_path):
    labels = ['white','empty','black']
    for label in labels:
        path = os.path.join(des_path, label)
        if not os.path.exists(path):
            os.mkdir(path)

def get_subdir(dir_path):
    return [os.path.join(dir_path, sub) for sub in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, sub))]

def load_images(dir_path):
    images = []
    for dirs in os.listdir(dir_path):
        fn, ext = os.path.splitext(dirs)
        if ext == '.jpg':
            images.append(os.path.join(dir_path,dirs))
    return images

def save_squares(board, board_state, des_path, data_i, board_i):
    for i in range(64):
        fn = '_'.join(['data',str(data_i),'board',str(board_i),str(i)]) + '.jpg'
        sq = board.square_at(i).img
        piece_type = board_state.piece_at(i)
        if piece_type in WHITE_PIECES:
            path = os.path.join(des_path, 'white',fn)
        elif piece_type in BLACK_PIECES:
            path = os.path.join(des_path, 'black',fn)
        else:
            path = os.path.join(des_path, 'empty',fn)
        cv2.imwrite(path, sq)

def main():
    raw_dir = "./data/raw_image"
    des_dir = "./data/squares/color"
    create_dir(des_dir)
    data_index = 0
    for raw_data_dir in get_subdir(raw_dir):
        images = load_images(raw_data_dir)
        board_index=0
        with open(os.path.join(raw_data_dir,'board.fen')) as f:
            fen = f.read()
            board_state = chess.BaseBoard(board_fen=fen)
        for image_path in images:
            print(image_path)
            board = Chessboard(cv2.imread(image_path))
            save_squares(board,board_state,des_dir, data_index, board_index)
            board_index += 1
        data_index += 1

main()
        

