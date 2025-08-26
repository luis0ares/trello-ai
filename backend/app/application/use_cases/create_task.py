from app.application.dtos.task_dto import TaskCreateDTO, TaskDTO
from app.domain.models.task import TaskCreateModel
from app.domain.repositories.board_repository import BoardRepository
from app.domain.repositories.task_repository import TaskRepository


class CreateTaskUseCase:
    def __init__(self, board_repository: BoardRepository,
                 task_repository: TaskRepository):
        self.board_repository = board_repository
        self.task_repository = task_repository

    async def execute(self, task_data: TaskCreateDTO) -> TaskDTO:
        """
        Create a new task with the provided data.

        :param task_data: object containing the task details.
        :return: The created task object.
        """
        if not isinstance(task_data, TaskCreateDTO):
            raise ValueError("Invalid payload type")

        board = await self.board_repository.get_by_external_id(
            task_data.board_id)
        if not board:
            # TODO: Custom exception for not found and an exeption handler
            raise ValueError("Board not found")

        # Create the task using the repository
        to_create = TaskCreateModel(
            board_id=board.id,
            title=task_data.title,
            description=task_data.description,
            position=task_data.position,
        )

        created_task = await self.task_repository.create(to_create)

        return TaskDTO(
            id=str(created_task.external_id),
            board_id=str(board.external_id),
            title=created_task.title,
            description=created_task.description,
            position=created_task.position,
            created_at=created_task.created_at,
            updated_at=created_task.updated_at
        )
