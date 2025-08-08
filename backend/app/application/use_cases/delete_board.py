from app.domain.repositories.board_repository import BoardRepository


class DeleteBoardUseCase:
    def __init__(self, board_repository: BoardRepository):
        self.board_repository = board_repository

    async def execute(self, board_id: str) -> bool:
        """
        Execute the use case to delete a board by its external ID.

        :param board_id: The external ID of the board to delete.
        :return: True if deletion was successful, otherwise False.
        """
        return await self.board_repository.delete(board_id)
