from logging import Logger

from app.domain.repositories.task_repository import TaskRepository


class DeleteTaskUseCase:
    def __init__(self, logger: Logger, task_repository: TaskRepository):
        self.logger = logger
        self.task_repository = task_repository

    async def execute(self, task_id: str) -> bool:
        """
        Execute the use case to delete a task by its external ID.

        :param task_id: The external ID of the task to delete.
        :return: True if deletion was successful, otherwise False.
        """
        self.logger.debug("Deleting task with external ID: {task_id}")
        has_deleted = await self.task_repository.delete(task_id)
        self.logger.info(
            f"Task with external ID {task_id} deleted: {has_deleted}")
        return has_deleted
