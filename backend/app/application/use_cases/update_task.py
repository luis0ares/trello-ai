from dataclasses import asdict
from logging import Logger

from app.application.dtos.task_dto import TaskDTO, TaskUpdateDTO
from app.core.exceptions import ResourseNotFound
from app.domain.models.task import TaskUpdateModel
from app.domain.repositories.board_repository import BoardRepository
from app.domain.repositories.task_repository import TaskRepository


class UpdateTaskUseCase:
    def __init__(self, logger: Logger, board_repository: BoardRepository,
                 task_repository: TaskRepository):
        self.logger = logger
        self.board_repository = board_repository
        self.task_repository = task_repository

    async def execute(self, task_id: int,
                      task_data: TaskUpdateDTO) -> TaskDTO:
        """
        Update an existing task with the provided data.

        :param task_id: The external ID of the task to update.
        :param task_data: object containing the updated task details.
        :return: The updated task object.
        """
        if not isinstance(task_data, TaskUpdateDTO):
            raise ValueError("Invalid payload type")
        self.logger.debug(
            f"Updating task with external ID: {task_id} - {asdict(task_data)}")

        board = await self.board_repository.get_by_external_id(
            task_data.board_id)
        if not board:
            raise ResourseNotFound("Board not found")

        to_update = TaskUpdateModel(
            board_id=board.id,
            title=task_data.title,
            description=task_data.description,
            position=task_data.position,
        )

        updated = await self.task_repository.update(task_id, to_update)
        self.logger.info(
            f"Task with external ID {updated.external_id} updated.")
        self.logger.debug(f"Updated task: {asdict(updated)}")

        return TaskDTO(
            id=str(updated.external_id),
            board_id=str(board.external_id),
            title=updated.title,
            description=updated.description,
            position=updated.position,
            created_at=updated.created_at,
            updated_at=updated.updated_at
        )
