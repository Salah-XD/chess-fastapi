from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from app.chess_logic import calculate_valid_moves

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
