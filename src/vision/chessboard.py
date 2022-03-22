import numpy as np
from .constant import SQUARE_SIZE, BOARD_SIZE
from .square import Square
class Chessboard():
    def __init__(self, img):
        self.img = img

    def square_at(self, index):
        y = int(BOARD_SIZE - ((index // 8) % 8) * SQUARE_SIZE - SQUARE_SIZE)
        x = (index % 8) * SQUARE_SIZE
        return Square(index, self.img[y:y+SQUARE_SIZE,x:x+SQUARE_SIZE,:])