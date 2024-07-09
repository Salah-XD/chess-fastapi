def is_valid_position(pos):
    return len(pos) == 2 and 'A' <= pos[0] <= 'H' and '1' <= pos[1] <= '8'

def get_valid_moves(piece, positions):
    piece_position = positions.get(piece.capitalize())
    if not piece_position or not is_valid_position(piece_position):
        return []

    valid_moves = []

    if piece == "queen":
        valid_moves = get_queen_moves(piece_position, positions)
    elif piece == "bishop":
        valid_moves = get_bishop_moves(piece_position, positions)
    elif piece == "rook":
        valid_moves = get_rook_moves(piece_position, positions)
    elif piece == "knight":
        valid_moves = get_knight_moves(piece_position, positions)

    return valid_moves

def get_queen_moves(pos, positions):
    moves = get_rook_moves(pos, positions) + get_bishop_moves(pos, positions)
    return list(set(moves))  # Remove duplicates

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
                    moves.append(new_pos)
                    break
                moves.append(new_pos)
            else:
                break
    return moves

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

def is_under_attack(pos, positions):
    for piece, piece_pos in positions.items():
        if piece == "Knight":
            continue  # Skip the knight itself
        if piece == "Queen":
            if pos in get_queen_moves(piece_pos, positions):
                return True
        elif piece == "Bishop":
            if pos in get_bishop_moves(piece_pos, positions):
                return True
        elif piece == "Rook":
            if pos in get_rook_moves(piece_pos, positions):
                return True
    return False