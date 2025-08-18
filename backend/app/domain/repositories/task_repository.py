from abc import ABC, abstractmethod
from typing import List

from app.domain.models.task import (
    TaskCreateModel,
    TaskModel,
    TaskUpdateModel,
)


class TaskRepository(ABC):
    @abstractmethod
    async def create(self, task_data: TaskCreateModel) -> TaskModel:
        """
        Create a new task with the provided data.

        :param task_data: TaskModel containing the task details.
        :return: The created task object.
        """
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    async def get_all(self) -> List[TaskModel]:
        """
        Retrieve all tasks.

        :return: A list containing all tasks objects found.
        """
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    async def update(self, task_id: int,
                     task_data: TaskUpdateModel) -> TaskModel:
        """
        Update an existing task with the provided data.

        :param task_id: The external ID of the task to update.
        :param task_data: object containing the updated task details.
        :return: The updated task object.
        """
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    async def delete(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        :param task_id: The external ID of the task to delete.
        :return: True if deletion was successful, otherwise False.
        """
        raise NotImplementedError("Method not implemented")
