from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List

app = FastAPI()

class ChessRequest(BaseModel):
    positions: Dict[str, str]

@app.post("/chess/{piece}")
def get_valid_moves(piece: str, request: ChessRequest):
    positions = request.positions
    piece = piece.lower()

    if piece.capitalize() not in positions:
        raise HTTPException(status_code=404, detail="Piece not found in positions")

    piece_position = positions[piece.capitalize()]
    valid_moves = calculate_valid_moves(piece, piece_position, positions)

    return {"valid_moves": valid_moves}

def calculate_valid_moves(piece: str, position: str, positions: Dict[str, str]) -> List[str]:
    row, col = ord(position[0].upper()) - ord('A'), int(position[1]) - 1
    directions = {
        'queen': queen_moves,
        'rook': rook_moves,
        'bishop': bishop_moves,
        'knight': knight_moves,
    }

    if piece in directions:
        return directions[piece](row, col, positions)
    else:
        raise HTTPException(status_code=400, detail="Unsupported piece type")

def queen_moves(row, col, positions):
    return rook_moves(row, col, positions) + bishop_moves(row, col, positions)

def rook_moves(row, col, positions):
    moves = []
    for i in range(8):
        if i != row:
            moves.append(chr(i + ord('A')) + str(col + 1))
        if i != col:
            moves.append(chr(row + ord('A')) + str(i + 1))
    return moves

def bishop_moves(row, col, positions):
    moves = []
    for i in range(8):
        if i != 0:
            if 0 <= row + i < 8 and 0 <= col + i < 8:
                moves.append(chr(row + i + ord('A')) + str(col + i + 1))
            if 0 <= row + i < 8 and 0 <= col - i < 8:
                moves.append(chr(row + i + ord('A')) + str(col - i + 1))
            if 0 <= row - i < 8 and 0 <= col + i < 8:
                moves.append(chr(row - i + ord('A')) + str(col + i + 1))
            if 0 <= row - i < 8 and 0 <= col - i < 8:
                moves.append(chr(row - i + ord('A')) + str(col - i + 1))
    return moves

def knight_moves(row, col, positions):
    moves = []
    knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
    for dr, dc in knight_moves:
        if 0 <= row + dr < 8 and 0 <= col + dc < 8:
            moves.append(chr(row + dr + ord('A')) + str(col + dc + 1))
    return moves
