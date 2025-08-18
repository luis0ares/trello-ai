
from fastapi import APIRouter

from app.application.dtos.task_dto import TaskCreateDTO, TaskUpdateDTO
from app.application.use_cases.create_task import CreateTaskUseCase
from app.application.use_cases.delete_task import DeleteTaskUseCase
from app.application.use_cases.update_task import UpdateTaskUseCase
from app.presentation.dependencies import BoardRepository, TaskRepository
from app.presentation.schemas.tasks import (
    TaskCreate,
    TaskResponse,
    TaskUpdate,
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("", response_model=TaskResponse, status_code=201)
async def create_task(payload: TaskCreate,
                      board_repository: BoardRepository,
                      task_repository: TaskRepository):
    task = TaskCreateDTO(
        board_id=int(payload.board_id),
        title=payload.title,
        description=payload.description,
        position=payload.position
    )

    use_case = CreateTaskUseCase(board_repository, task_repository)
    created_task = await use_case.execute(task)

    return TaskResponse(
        id=created_task.id,
        board_id=created_task.board_id,
        title=created_task.title,
        description=created_task.description,
        position=created_task.position,
        created_at=created_task.created_at,
        updated_at=created_task.updated_at
    )


@router.put("/{id}", response_model=TaskResponse)
async def update_task(id: str, payload: TaskUpdate,
                      board_repository: BoardRepository,
                      task_repository: TaskRepository):
    task = TaskUpdateDTO(
        board_id=int(payload.board_id),
        title=payload.title,
        description=payload.description,
        position=payload.position
    )

    use_case = UpdateTaskUseCase(board_repository, task_repository)
    updated_task = await use_case.execute(int(id), task)

    return TaskResponse(
        id=updated_task.id,
        board_id=updated_task.board_id,
        title=updated_task.title,
        description=updated_task.description,
        position=updated_task.position,
        created_at=updated_task.created_at,
        updated_at=updated_task.updated_at
    )


@router.delete("/{id}", status_code=204)
async def delete_task(id: str, task_repository: TaskRepository):
    use_case = DeleteTaskUseCase(task_repository)
    await use_case.execute(int(id))
