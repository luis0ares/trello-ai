from app.domain.repositories.task_repository import TaskRepository


class DeleteTaskUseCase:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    async def execute(self, task_id: str) -> bool:
        """
        Execute the use case to delete a task by its external ID.

        :param task_id: The external ID of the task to delete.
        :return: True if deletion was successful, otherwise False.
        """
        return await self.task_repository.delete(task_id)
