from typing import List, Dict
from fastapi import HTTPException

def calculate_valid_moves(piece: str, position: str, positions: Dict[str, str]) -> List[str]:
    row, col = ord(position[0].upper()) - ord('A'), int(position[1]) - 1
    directions = {
        'queen': queen_moves,
        'rook': rook_moves,
        'bishop': bishop_moves,
        'knight': knight_moves,
    }

    if piece in directions:
        potential_moves = directions[piece](row, col)
        return filter_valid_moves(piece, position, potential_moves, positions)
    else:
        raise HTTPException(status_code=400, detail="Unsupported piece type")

def filter_valid_moves(piece: str, position: str, moves: List[str], positions: Dict[str, str]) -> List[str]:
    valid_moves = []

    for move in moves:
        if not is_under_attack(piece, move, positions):
            valid_moves.append(move)

    return valid_moves

def is_under_attack(piece: str, target: str, positions: Dict[str, str]) -> bool:
    for enemy_piece, enemy_pos in positions.items():
        if enemy_piece.lower() != piece:
            if can_attack(enemy_piece.lower(), enemy_pos, target):
                return True
    return False

def can_attack(piece: str, pos: str, target: str) -> bool:
    row_pos, col_pos = ord(pos[0].upper()) - ord('A'), int(pos[1]) - 1
    row_target, col_target = ord(target[0].upper()) - ord('A'), int(target[1]) - 1

    if piece == 'queen':
        return can_attack_rook(row_pos, col_pos, row_target, col_target) or can_attack_bishop(row_pos, col_pos, row_target, col_target)
    elif piece == 'rook':
        return can_attack_rook(row_pos, col_pos, row_target, col_target)
    elif piece == 'bishop':
        return can_attack_bishop(row_pos, col_pos, row_target, col_target)
    elif piece == 'knight':
        return can_attack_knight(row_pos, col_pos, row_target, col_target)
    else:
        return False

def can_attack_rook(row_pos, col_pos, row_target, col_target):
    return row_pos == row_target or col_pos == col_target

def can_attack_bishop(row_pos, col_pos, row_target, col_target):
    return abs(row_pos - row_target) == abs(col_pos - col_target)

def can_attack_knight(row_pos, col_pos, row_target, col_target):
    return (abs(row_pos - row_target) == 2 and abs(col_pos - col_target) == 1) or \
           (abs(row_pos - row_target) == 1 and abs(col_pos - col_target) == 2)

def queen_moves(row, col):
    return rook_moves(row, col) + bishop_moves(row, col)

def rook_moves(row, col):
    moves = []
    for i in range(8):
        if i != row:
            moves.append(chr(i + ord('A')) + str(col + 1))
        if i != col:
            moves.append(chr(row + ord('A')) + str(i + 1))
    return moves

def bishop_moves(row, col):
    moves = []
    for i in range(1, 8):
        if 0 <= row + i < 8 and 0 <= col + i < 8:
            moves.append(chr(row + i + ord('A')) + str(col + i + 1))
        if 0 <= row + i < 8 and 0 <= col - i >= 0:
            moves.append(chr(row + i + ord('A')) + str(col - i + 1))
        if 0 <= row - i >= 0 and 0 <= col + i < 8:
            moves.append(chr(row - i + ord('A')) + str(col + i + 1))
        if 0 <= row - i >= 0 and 0 <= col - i >= 0:
            moves.append(chr(row - i + ord('A')) + str(col - i + 1))
    return moves

def knight_moves(row, col):
    moves = []
    knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
    for dr, dc in knight_moves:
        if 0 <= row + dr < 8 and 0 <= col + dc < 8:
            moves.append(chr(row + dr + ord('A')) + str(col + dc + 1))
    return moves
