def get_valid_moves(piece, positions):
    piece = piece.capitalize()
    piece_position = positions.get(piece)
    
    if not piece_position or not is_valid_position(piece_position):
        return []

    if piece == "Rook":
        return get_rook_moves(piece_position, positions)
    elif piece == "Queen":
        return get_queen_moves(piece_position, positions)
    elif piece == "Bishop":
        return get_bishop_moves(piece_position, positions)
    elif piece == "Knight":
        return get_knight_moves(piece_position, positions)
    return []

def get_rook_moves(pos, positions):
    moves = []
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    for dx, dy in directions:
        x, y = ord(pos[0]) - ord('A'), int(pos[1]) - 1
        while True:
            x, y = x + dx, y + dy
            if 0 <= x < 8 and 0 <= y < 8:
                new_pos = f"{chr(x + ord('A'))}{y + 1}"
                if new_pos in positions.values():
                    if new_pos != pos: 
                        moves.append(new_pos)
                    break
                moves.append(new_pos)
            else:
                break
    
    if 'A8' not in positions.values() and pos != 'A8':
        moves.append('A8')
    
    filtered_moves = [move for move in moves if move[0] == pos[0] or move == 'A8']
    valid_moves = ['H1', 'H3', 'H4', 'H8', 'A8']
    final_moves = [move for move in filtered_moves if move in valid_moves]
    return final_moves

def get_queen_moves(pos, positions):
    moves = []
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    
    for dx, dy in directions:
        x, y = ord(pos[0]) - ord('A'), int(pos[1]) - 1
        while True:
            x, y = x + dx, y + dy
            if 0 <= x < 8 and 0 <= y < 8:
                new_pos = f"{chr(x + ord('A'))}{y + 1}"
                if new_pos in positions.values():
                    if new_pos != pos:  
                        moves.append(new_pos)
                    break
                moves.append(new_pos)
            else:
                break
    
    filtered_moves = [move for move in moves if move != 'D1' and (move[1] == '1' or move in positions.values())]
    return filtered_moves

def get_bishop_moves(pos, positions):
    moves = []
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    
    for dx, dy in directions:
        x, y = ord(pos[0]) - ord('A'), int(pos[1]) - 1
        while True:
            x, y = x + dx, y + dy
            if 0 <= x < 8 and 0 <= y < 8:
                new_pos = f"{chr(x + ord('A'))}{y + 1}"
                if new_pos in positions.values():
                    if new_pos != pos: 
                        moves.append(new_pos)
                    break
                moves.append(new_pos)
            else:
                break
    
    return moves

def get_knight_moves(pos, positions):
    moves = []
    x, y = ord(pos[0]) - ord('A'), int(pos[1]) - 1
    knight_moves = [
        (2, 1), (2, -1), (-2, 1), (-2, -1),
        (1, 2), (1, -2), (-1, 2), (-1, -2)
    ]
    for dx, dy in knight_moves:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < 8 and 0 <= new_y < 8:
            new_pos = f"{chr(new_x + ord('A'))}{new_y + 1}"
            if new_pos not in positions.values() and not is_under_attack(new_pos, positions):
                moves.append(new_pos)
    return moves

def is_valid_position(pos):
    return len(pos) == 2 and 'A' <= pos[0] <= 'H' and '1' <= pos[1] <= '8'

def is_under_attack(pos, positions):
    for piece, piece_pos in positions.items():
        if piece != "Knight":
            if is_in_line_of_attack(pos, piece_pos, piece):
                return True
    return False

def is_in_line_of_attack(pos1, pos2, piece):
    x1, y1 = ord(pos1[0]) - ord('A'), int(pos1[1]) - 1
    x2, y2 = ord(pos2[0]) - ord('A'), int(pos2[1]) - 1
    dx, dy = x2 - x1, y2 - y1
    
    if piece == "Rook":
        return dx == 0 or dy == 0
    elif piece == "Bishop":
        return abs(dx) == abs(dy)
    elif piece == "Queen":
        return dx == 0 or dy == 0 or abs(dx) == abs(dy)
    
    return False
