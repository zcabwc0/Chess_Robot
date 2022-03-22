import chess
SQUARE_SIZE = 60
BOARD_SIZE = SQUARE_SIZE * 8
WHITE_PIECES = [chess.Piece(chess.PAWN, chess.WHITE), chess.Piece(chess.KNIGHT, chess.WHITE), 
    chess.Piece(chess.BISHOP, chess.WHITE), chess.Piece(chess.ROOK, chess.WHITE),chess.Piece(chess.KING, chess.WHITE),
    chess.Piece(chess.QUEEN, chess.WHITE)]
BLACK_PIECES = [chess.Piece(chess.PAWN, chess.BLACK), chess.Piece(chess.KNIGHT, chess.BLACK), 
    chess.Piece(chess.BISHOP, chess.BLACK), chess.Piece(chess.ROOK, chess.BLACK),chess.Piece(chess.KING, chess.BLACK),
    chess.Piece(chess.QUEEN, chess.BLACK)]
INDEX_TO_POSITION = ['a1','b1','c1','d1','e1','f1','g1','h1',
                    'a2','b2','c2','d2','e2','f2','g2','h2',
                    'a3','b3','c3','d3','e3','f3','g3','h3',
                    'a4','b4','c4','d4','e4','f4','g4','h4',
                    'a5','b5','c5','d5','e5','f5','g5','h5',
                    'a6','b6','c6','d6','e6','f6','g6','h6',
                    'a7','b7','c7','d7','e7','f7','g7','h7',
                    'a8','b8','c8','d8','e8','f8','g8','h8',]
EMPTY = 0
BLACK = 1
WHITE = 2