from typing import List

from app.application.dtos.board_dto import BoardDTO
from app.domain.repositories.board_repository import BoardRepository


class GetBoardsUseCase:
    def __init__(self, board_repository: BoardRepository):
        self.board_repository = board_repository

    async def execute(self) -> List[BoardDTO]:
        """
        Retrieves all boards.

        :return: A list of boards.
        """
        boards = await self.board_repository.get_all()
        return [BoardDTO(
            id=str(board.external_id),
            name=board.name,
            position=board.position,
            created_at=board.created_at,
            updated_at=board.updated_at
        ) for board in boards]
