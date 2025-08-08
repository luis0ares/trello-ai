from typing import List
from fastapi import APIRouter

from app.presentation.schemas.boards import BoardCreate, BoardResponse, BoardUpdate

router = APIRouter(prefix="/boards", tags=["Boards"])


@router.get("/", response_model=List[BoardResponse])
async def get_boards():
    return [{"message": "List of boards"}]


@router.post("/", response_model=BoardResponse, status_code=201)
async def create_board(board: BoardCreate):
    return {"message": "Board created", "board": board}


@router.put("/{id}", response_model=BoardResponse)
async def update_board(id: str, board: BoardUpdate):
    return {"message": "Board updated", "board_id": id, "board": board}


@router.delete("/{id}", status_code=204)
async def delete_board(id: str):
    return {"message": "Board deleted", "board_id": id}
