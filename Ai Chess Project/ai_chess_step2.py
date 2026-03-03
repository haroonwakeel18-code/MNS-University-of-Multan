# ai_chess_step2.py

# Same piece values and board
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

piece_values = {'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9, 'k': float('inf')}
piece_names = {'P': 'Pawn', 'N': 'Knight', 'B': 'Bishop', 'R': 'Rook', 'Q': 'Queen', 'K': 'King'}
cols = 'abcdefgh'

def is_enemy(piece):
    return piece.islower()

def in_bounds(r, c):
    return 0 <= r < 8 and 0 <= c < 8

def add_move(moves, board, r, c, r2, c2, piece):
    target = board[r2][c2]
    score = piece_values.get(target.lower(), 0) if is_enemy(target) else 0
    if target == '.' or is_enemy(target):
        moves.append({
            'from': (r, c),
            'to': (r2, c2),
            'target': target,
            'score': score,
            'piece': piece
        })

def get_moves_for_piece(board, r, c):
    piece = board[r][c]
    if not piece.isupper():
        return []
    moves = []
    directions = []

    if piece == 'P':  # Pawn
        if in_bounds(r-1, c) and board[r-1][c] == '.':
            add_move(moves, board, r, c, r-1, c, piece)
        for dc in [-1, 1]:
            nr, nc = r-1, c+dc
            if in_bounds(nr, nc) and is_enemy(board[nr][nc]):
                add_move(moves, board, r, c, nr, nc, piece)

    elif piece == 'N':  # Knight
        knight_moves = [(2, 1), (1, 2), (-1, 2), (-2, 1),
                        (-2, -1), (-1, -2), (1, -2), (2, -1)]
        for dr, dc in knight_moves:
            nr, nc = r+dr, c+dc
            if in_bounds(nr, nc):
                add_move(moves, board, r, c, nr, nc, piece)

    elif piece == 'B':  # Bishop
        directions = [(-1,-1), (-1,1), (1,-1), (1,1)]

    elif piece == 'R':  # Rook
        directions = [(-1,0), (1,0), (0,-1), (0,1)]

    elif piece == 'Q':  # Queen
        directions = [(-1,-1), (-1,1), (1,-1), (1,1), (-1,0), (1,0), (0,-1), (0,1)]

    elif piece == 'K':  # King
        directions = [(-1,-1), (-1,1), (1,-1), (1,1), (-1,0), (1,0), (0,-1), (0,1)]
        for dr, dc in directions:
            nr, nc = r+dr, c+dc
            if in_bounds(nr, nc):
                add_move(moves, board, r, c, nr, nc, piece)
        return moves

    # For sliding pieces (Bishop, Rook, Queen)
    for dr, dc in directions:
        nr, nc = r+dr, c+dc
        while in_bounds(nr, nc):
            target = board[nr][nc]
            add_move(moves, board, r, c, nr, nc, piece)
            if target != '.':
                break
            nr += dr
            nc += dc

    return moves

# Find all white piece moves
def get_all_white_moves(board):
    moves = []
    for r in range(8):
        for c in range(8):
            if board[r][c].isupper():
                moves.extend(get_moves_for_piece(board, r, c))
    return moves

def select_best_move(moves):
    return max(moves, key=lambda m: m['score'], default=None)

def format_move(move):
    r, c = move['to']
    return f"{piece_names[move['piece']]}{cols[c]}{8 - r}"

# MAIN
moves = get_all_white_moves(board)
best_move = select_best_move(moves)

if best_move:
    print("Best move:", format_move(best_move))
else:
    print("No legal moves available.")
