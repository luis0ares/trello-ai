from abc import ABC, abstractmethod
from typing import List

from app.domain.models.board import BoardModel


class BoardRepository(ABC):
    @abstractmethod
    async def create(self, board_data: BoardModel) -> BoardModel:
        """
        Create a new board with the provided data.
        
        :param board_data: BoardModel containing the board details.
        :return: The created board object.
        """
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    async def get_all(self) -> List[BoardModel]:
        """
        Retrieve all boards.
        
        :return: A list containing all boards objects found.
        """
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    async def update(self, board_id: str, board_data: BoardModel) -> BoardModel:
        """
        Update an existing board with the provided data.
        
        :param board_id: The external ID of the board to update.
        :param board_data: BoardModel containing the updated board details.
        :return: The updated board object.
        """
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    async def delete(self, board_id: str) -> bool:
        """
        Delete a board by its external ID.
        
        :param board_id: The external ID of the board to delete.
        :return: True if deletion was successful, otherwise False.
        """
        raise NotImplementedError("Method not implemented")