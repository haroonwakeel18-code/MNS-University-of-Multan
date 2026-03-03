# ai_chess_test.py

# Define board pieces (uppercase = white, lowercase = black)
# Empty squares are "."
board = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
    ['p', 'p', 'p', 'p', '.', 'p', 'p', 'p'],
    ['.', '.', '.', '.', 'p', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', 'P', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['P', 'P', 'P', 'P', '.', 'P', 'P', 'P'],
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
]

# Piece values
piece_values = {
    'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9, 'k': float('inf')
}

# Piece names
piece_names = {
    'P': 'Pawn', 'N': 'Knight', 'B': 'Bishop', 'R': 'Rook', 'Q': 'Queen', 'K': 'King'
}

# Map indices to board columns
cols = 'abcdefgh'

# Get all possible moves for white pawns (basic version)
def get_white_moves(board):
    moves = []

    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece.isupper():  # White piece
                piece_type = piece
                # Check diagonals for captures (simple rule)
                for dr, dc in [(-1, -1), (-1, 1)]:  # only upward diagonals
                    r, c = row + dr, col + dc
                    if 0 <= r < 8 and 0 <= c < 8:
                        target = board[r][c]
                        if target.islower():  # Capturable black piece
                            move = {
                                'from': (row, col),
                                'to': (r, c),
                                'target': target,
                                'score': piece_values.get(target.lower(), 0),
                                'piece': piece
                            }
                            moves.append(move)
    return moves

# Select best move based on score
def select_best_move(moves):
    if not moves:
        return None
    return max(moves, key=lambda m: m['score'])

# Convert move to format: PieceName + target square
def format_move(move):
    row, col = move['to']
    name = piece_names[move['piece']]
    square = cols[col] + str(8 - row)
    return f"{name}{square}"

# MAIN
moves = get_white_moves(board)
best_move = select_best_move(moves)

if best_move:
    print("Best move:", format_move(best_move))
else:
    print("No capture moves available.")
