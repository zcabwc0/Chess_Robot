import chess

# Initialising the chess game FEN
fen_path = "current_game.fen"
init_fen = chess.STARTING_FEN
with open(fen_path, 'w') as f:
    f.write(init_fen)