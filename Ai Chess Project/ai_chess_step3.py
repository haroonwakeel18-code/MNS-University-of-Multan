# ai_chess_step3.py

import copy

# Board setup (white uppercase, black lowercase)
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
piece_names = {
    'P': 'Pawn', 'N': 'Knight', 'B': 'Bishop', 'R': 'Rook', 'Q': 'Queen', 'K': 'King',
    'p': 'Pawn', 'n': 'Knight', 'b': 'Bishop', 'r': 'Rook', 'q': 'Queen', 'k': 'King'
}
cols = 'abcdefgh'

def is_enemy(piece, white_turn):
    if piece == '.':
        return False
    return piece.islower() if white_turn else piece.isupper()

def is_friend(piece, white_turn):
    if piece == '.':
        return False
    return piece.isupper() if white_turn else piece.islower()

def in_bounds(r, c):
    return 0 <= r < 8 and 0 <= c < 8

def add_move(moves, board, r, c, r2, c2, piece, white_turn):
    target = board[r2][c2]
    if target == '.' or is_enemy(target, white_turn):
        score = piece_values.get(target.lower(), 0) if is_enemy(target, white_turn) else 0
        moves.append({
            'from': (r, c),
            'to': (r2, c2),
            'target': target,
            'score': score,
            'piece': piece
        })

def get_moves_for_piece(board, r, c, white_turn):
    piece = board[r][c]
    if not is_friend(piece, white_turn):
        return []
    moves = []
    directions = []

    if piece.lower() == 'p':  # Pawn
        dir = -1 if white_turn else 1
        start_row = 6 if white_turn else 1
        # Move forward
        if in_bounds(r + dir, c) and board[r + dir][c] == '.':
            add_move(moves, board, r, c, r + dir, c, piece, white_turn)
            # Double move from start
            if r == start_row and board[r + 2 * dir][c] == '.':
                add_move(moves, board, r, c, r + 2 * dir, c, piece, white_turn)
        # Captures
        for dc in [-1, 1]:
            nr, nc = r + dir, c + dc
            if in_bounds(nr, nc) and is_enemy(board[nr][nc], white_turn):
                add_move(moves, board, r, c, nr, nc, piece, white_turn)

    elif piece.lower() == 'n':  # Knight
        for dr, dc in [(2, 1), (1, 2), (-1, 2), (-2, 1),
                       (-2, -1), (-1, -2), (1, -2), (2, -1)]:
            nr, nc = r + dr, c + dc
            if in_bounds(nr, nc):
                add_move(moves, board, r, c, nr, nc, piece, white_turn)

    elif piece.lower() in ['b', 'r', 'q']:
        if piece.lower() == 'b':
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        elif piece.lower() == 'r':
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        elif piece.lower() == 'q':
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            while in_bounds(nr, nc):
                if is_friend(board[nr][nc], white_turn):
                    break
                add_move(moves, board, r, c, nr, nc, piece, white_turn)
                if is_enemy(board[nr][nc], white_turn):
                    break
                nr += dr
                nc += dc

    elif piece.lower() == 'k':
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if in_bounds(nr, nc):
                    add_move(moves, board, r, c, nr, nc, piece, white_turn)

    return moves

def get_all_moves(board, white_turn):
    moves = []
    for r in range(8):
        for c in range(8):
            if is_friend(board[r][c], white_turn):
                moves += get_moves_for_piece(board, r, c, white_turn)
    return moves

def select_best_move(moves):
    return max(moves, key=lambda m: m['score'], default=None)

def format_move(move):
    r, c = move['to']
    return f"{piece_names[move['piece']]}{cols[c]}{8 - r}"

def make_move(board, move):
    r1, c1 = move['from']
    r2, c2 = move['to']
    board[r2][c2] = board[r1][c1]
    board[r1][c1] = '.'

def print_board(board):
    for row in board:
        print(' '.join(row))
    print()

# MAIN LOOP
white_turn = True
turns = 10  # Simulate 10 turns
for i in range(turns):
    print(f"\nTurn {i+1} - {'White' if white_turn else 'Black'} to move")
    print_board(board)

    moves = get_all_moves(board, white_turn)
    move = select_best_move(moves)

    if not move:
        print("No legal moves available.")
        break

    print("Move:", format_move(move))
    make_move(board, move)
    white_turn = not white_turn
