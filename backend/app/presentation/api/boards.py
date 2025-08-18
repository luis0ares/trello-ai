from typing import List

from fastapi import APIRouter

from app.application.dtos.board_dto import BoardCreateDTO, BoardUpdateDTO
from app.application.use_cases.create_board import CreateBoardUseCase
from app.application.use_cases.delete_board import DeleteBoardUseCase
from app.application.use_cases.get_boards import GetBoardsUseCase
from app.application.use_cases.update_board import UpdateBoardUseCase
from app.presentation.dependencies import BoardRepository, TaskRepository
from app.presentation.schemas.boards import (
    BoardCreate,
    BoardResponse,
    BoardUpdate,
)
from app.presentation.schemas.tasks import TaskResponse

router = APIRouter(prefix="/boards", tags=["Boards"])


@router.get("", response_model=List[BoardResponse])
async def get_boards(
        board_repository: BoardRepository, task_repository: TaskRepository):
    use_case = GetBoardsUseCase(board_repository, TaskRepository)
    boards = await use_case.execute()

    return [BoardResponse(
        id=board.id,
        name=board.name,
        position=board.position,
        created_at=board.created_at,
        updated_at=board.updated_at,
        tasks=[TaskResponse(
            id=task.id,
            board_id=task.board_id,
            title=task.title,
            description=task.description,
            position=task.position,
            created_at=task.created_at,
            updated_at=task.updated_at
        ) for task in board.tasks]
    ) for board in boards]


@router.post("", response_model=BoardResponse, status_code=201)
async def create_board(payload: BoardCreate,
                       board_repository: BoardRepository):
    board = BoardCreateDTO(name=payload.name, position=payload.position)

    use_case = CreateBoardUseCase(board_repository)
    created_board = await use_case.execute(board)

    return BoardResponse(
        id=created_board.id,
        name=created_board.name,
        position=created_board.position,
        created_at=created_board.created_at,
        updated_at=created_board.updated_at
    )


@router.put("/{id}", response_model=BoardResponse)
async def update_board(id: str, payload: BoardUpdate,
                       board_repository: BoardRepository):
    board = BoardUpdateDTO(name=payload.name, position=payload.position)

    use_case = UpdateBoardUseCase(board_repository)
    updated_board = await use_case.execute(int(id), board)

    return BoardResponse(
        id=updated_board.id,
        name=updated_board.name,
        position=updated_board.position,
        created_at=updated_board.created_at,
        updated_at=updated_board.updated_at
    )


@router.delete("/{id}", status_code=204)
async def delete_board(id: str, board_repository: BoardRepository):
    use_case = DeleteBoardUseCase(board_repository)
    await use_case.execute(int(id))
