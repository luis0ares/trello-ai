from abc import ABC, abstractmethod
from typing import List

from app.domain.models.board import (
    BoardCreateModel,
    BoardModel,
    BoardUpdateModel,
    BoardWithTasksModel,
)


class BoardRepository(ABC):
    @abstractmethod
    async def create(self, board_data: BoardCreateModel) -> BoardModel:
        """
        Create a new board with the provided data.

        :param board_data: BoardModel containing the board details.
        :return: The created board object.
        """
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    async def get_all(self) -> List[BoardWithTasksModel]:
        """
        Retrieve all boards with their associated tasks.

        :return: A list containing all boards objects found.
        """
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    async def get_by_external_id(self, external_id: int) -> BoardModel | None:
        """
        Retrieve a board by its external ID.

        :param external_id: The external ID of the board to retrieve.
        :return: The board object if found, otherwise None.
        """
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    async def update(self, board_id: int,
                     board_data: BoardUpdateModel) -> BoardModel:
        """
        Update an existing board with the provided data.

        :param board_id: The external ID of the board to update.
        :param board_data: object containing the updated board details.
        :return: The updated board object.
        """
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    async def delete(self, board_id: int) -> bool:
        """
        Delete a board by its ID.

        :param board_id: The external ID of the board to delete.
        :return: True if deletion was successful, otherwise False.
        """
        raise NotImplementedError("Method not implemented")
