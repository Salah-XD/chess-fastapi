
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.chess_logic import get_valid_moves

app = FastAPI()

class ChessPositions(BaseModel):
    positions: dict[str, str]

@app.post("/chess/{piece}")
async def get_chess_moves(piece: str, positions: ChessPositions):
    valid_pieces = ["queen", "bishop", "rook", "knight"]
    if piece.lower() not in valid_pieces:
        raise HTTPException(status_code=400, detail="Invalid chess piece")
    
    valid_moves = get_valid_moves(piece.lower(), positions.positions)
    return {"valid_moves": valid_moves}