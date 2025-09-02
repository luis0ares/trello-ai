from dataclasses import asdict
from logging import Logger

from app.application.dtos.task_dto import TaskCreateDTO, TaskDTO
from app.core.exceptions import ResourseNotFound
from app.domain.models.task import TaskCreateModel
from app.domain.repositories.board_repository import BoardRepository
from app.domain.repositories.task_repository import TaskRepository


class CreateTaskUseCase:
    def __init__(self, logger: Logger, board_repository: BoardRepository,
                 task_repository: TaskRepository):
        self.logger = logger
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
        self.logger.debug(f"Received task data: {asdict(task_data)}")

        board = await self.board_repository.get_by_external_id(
            task_data.board_id)
        if not board:
            self.logger.info(
                f"Board with external ID {task_data.board_id} not found")
            raise ResourseNotFound("Board not found")

        # Create the task using the repository
        to_create = TaskCreateModel(
            board_id=board.id,
            title=task_data.title,
            description=task_data.description,
            position=task_data.position,
        )

        created_task = await self.task_repository.create(to_create)
        self.logger.debug(f"Created task: {asdict(created_task)}")
        self.logger.info(
            f"Task created successfully. - Id: {created_task.id}")

        return TaskDTO(
            id=str(created_task.external_id),
            board_id=str(board.external_id),
            title=created_task.title,
            description=created_task.description,
            position=created_task.position,
            created_at=created_task.created_at,
            updated_at=created_task.updated_at
        )
