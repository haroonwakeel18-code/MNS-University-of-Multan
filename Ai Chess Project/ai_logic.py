import copy

piece_values = {
    'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9, 'k': 100
}

def is_enemy(piece, white_turn):
    return piece.islower() if white_turn else piece.isupper()

def is_friend(piece, white_turn):
    return piece.isupper() if white_turn else piece.islower()

def in_bounds(r, c):
    return 0 <= r < 8 and 0 <= c < 8

def get_moves_for_piece(board, r, c, white_turn):
    piece = board[r][c].lower()
    moves = []
    
    # Pawn moves
    if piece == 'p':
        direction = -1 if white_turn else 1
        start_row = 6 if white_turn else 1
        
        # Forward move
        if in_bounds(r + direction, c) and board[r + direction][c] == '.':
            moves.append((r + direction, c))
            # Double move from starting position
            if r == start_row and board[r + 2*direction][c] == '.':
                moves.append((r + 2*direction, c))
        
        # Captures
        for dc in [-1, 1]:
            if in_bounds(r + direction, c + dc):
                target = board[r + direction][c + dc]
                if target != '.' and is_enemy(target, white_turn):
                    moves.append((r + direction, c + dc))

    # Knight moves
    elif piece == 'n':
        for dr, dc in [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]:
            nr, nc = r + dr, c + dc
            if in_bounds(nr, nc) and not is_friend(board[nr][nc], white_turn):
                moves.append((nr, nc))

    # Bishop/Queen moves
    elif piece in ['b', 'q']:
        for dr, dc in [(1,1),(1,-1),(-1,1),(-1,-1)]:
            nr, nc = r + dr, c + dc
            while in_bounds(nr, nc):
                if not is_friend(board[nr][nc], white_turn):
                    moves.append((nr, nc))
                    if is_enemy(board[nr][nc], white_turn):
                        break
                else:
                    break
                nr += dr
                nc += dc

    # Rook/Queen moves
    if piece in ['r', 'q']:
        for dr, dc in [(1,0),(0,1),(-1,0),(0,-1)]:
            nr, nc = r + dr, c + dc
            while in_bounds(nr, nc):
                if not is_friend(board[nr][nc], white_turn):
                    moves.append((nr, nc))
                    if is_enemy(board[nr][nc], white_turn):
                        break
                else:
                    break
                nr += dr
                nc += dc

    # King moves
    elif piece == 'k':
        for dr in [-1,0,1]:
            for dc in [-1,0,1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if in_bounds(nr, nc) and not is_friend(board[nr][nc], white_turn):
                    moves.append((nr, nc))
    
    return moves

def get_all_moves(board, white_turn):
    moves = []
    for r in range(8):
        for c in range(8):
            if is_friend(board[r][c], white_turn):
                for nr, nc in get_moves_for_piece(board, r, c, white_turn):
                    target = board[nr][nc]
                    score = piece_values.get(target.lower(), 0) if is_enemy(target, white_turn) else 0
                    moves.append({
                        'from': (c, r),  # (x,y) format
                        'to': (nc, nr),
                        'piece': board[r][c].lower(),
                        'score': score
                    })
    return moves

def select_best_move_minimax(board, white_turn):
    moves = get_all_moves(board, white_turn)
    if not moves:
        return None
    
    best_move = None
    best_score = -float('inf')
    
    for move in moves:
        # Evaluate based on immediate material gain
        current_score = move['score']
        
        # Simple 1-ply lookahead
        new_board = copy.deepcopy(board)
        from_col, from_row = move['from']
        to_col, to_row = move['to']
        new_board[to_row][to_col] = new_board[from_row][from_col]
        new_board[from_row][from_col] = '.'
        
        opponent_moves = get_all_moves(new_board, not white_turn)
        if opponent_moves:
            # Find opponent's best response
            opponent_best = max(opponent_moves, key=lambda m: m['score'])
            current_score -= opponent_best['score'] * 0.5  # Discount future threat
        
        if current_score > best_score:
            best_score = current_score
            best_move = move
    
    return best_move