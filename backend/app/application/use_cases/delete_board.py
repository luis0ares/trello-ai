from logging import Logger

from app.domain.repositories.board_repository import BoardRepository


class DeleteBoardUseCase:
    def __init__(self, logger: Logger, board_repository: BoardRepository):
        self.logger = logger
        self.board_repository = board_repository

    async def execute(self, board_id: str) -> bool:
        """
        Execute the use case to delete a board by its external ID.

        :param board_id: The external ID of the board to delete.
        :return: True if deletion was successful, otherwise False.
        """
        self.logger.debug("Deleting board with external ID: {board_id}")
        has_deleted = await self.board_repository.delete(board_id)
        self.logger.info(
            f"Board with external ID {board_id} deleted: {has_deleted}")
        return has_deleted
