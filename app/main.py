from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List

app = FastAPI()

class ChessPositions(BaseModel):
    positions: Dict[str, str]

def is_valid_position(position: str) -> bool:
    return len(position) == 2 and position[0] in 'ABCDEFGH' and position[1] in '12345678'

def get_knight_moves(position: str) -> List[str]:
    col, row = position[0], int(position[1])
    moves = [
        (2, 1), (2, -1), (-2, 1), (-2, -1),
        (1, 2), (1, -2), (-1, 2), (-1, -2)
    ]
    valid_moves = []
    for dc, dr in moves:
        new_col = chr(ord(col) + dc)
        new_row = row + dr
        new_pos = f"{new_col}{new_row}"
        if is_valid_position(new_pos):
            valid_moves.append(new_pos)
    return valid_moves

def get_rook_moves(position: str, positions: Dict[str, str]) -> List[str]:
    col, row = position[0], int(position[1])
    valid_moves = []
    
    # Horizontal moves
    for c in 'ABCDEFGH':
        if c != col:
            new_pos = f"{c}{row}"
            if new_pos not in positions.values() or new_pos in positions.values():
                valid_moves.append(new_pos)
                if new_pos in positions.values():
                    break
    
    # Vertical moves
    for r in range(1, 9):
        if r != row:
            new_pos = f"{col}{r}"
            if new_pos not in positions.values() or new_pos in positions.values():
                valid_moves.append(new_pos)
                if new_pos in positions.values():
                    break
    
    return valid_moves

def get_queen_moves(position: str, positions: Dict[str, str]) -> List[str]:
    rook_moves = get_rook_moves(position, positions)
    bishop_moves = get_bishop_moves(position, positions)
    return list(set(rook_moves + bishop_moves))

def get_bishop_moves(position: str, positions: Dict[str, str]) -> List[str]:
    col, row = position[0], int(position[1])
    valid_moves = []
    
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    
    for dc, dr in directions:
        new_col, new_row = ord(col) - ord('A'), row - 1
        while True:
            new_col += dc
            new_row += dr
            if 0 <= new_col < 8 and 0 <= new_row < 8:
                new_pos = f"{chr(new_col + ord('A'))}{new_row + 1}"
                if new_pos not in positions.values() or new_pos in positions.values():
                    valid_moves.append(new_pos)
                    if new_pos in positions.values():
                        break
            else:
                break
    
    return valid_moves

@app.post("/chess/{piece}")
async def get_valid_moves(piece: str, chess_positions: ChessPositions):
    piece = piece.lower()
    positions = {k.lower(): v for k, v in chess_positions.positions.items()}
    
    if piece not in positions:
        raise HTTPException(status_code=400, detail=f"{piece.capitalize()} position not provided")
    
    position = positions[piece]
    
    if not is_valid_position(position):
        raise HTTPException(status_code=400, detail=f"Invalid position for {piece}: {position}")
    
    if piece == "knight":
        valid_moves = get_knight_moves(position)
    elif piece == "rook":
        valid_moves = get_rook_moves(position, positions)
    elif piece == "queen":
        valid_moves = get_queen_moves(position, positions)
    elif piece == "bishop":
        valid_moves = get_bishop_moves(position, positions)
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported piece: {piece}")
    
    return {"valid_moves": valid_moves}