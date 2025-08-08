from app.application.dtos.board_dto import BoardDTO
from app.domain.models.board import BoardModel
from app.domain.repositories.board_repository import BoardRepository


class UpdateBoardUseCase:
    def __init__(self, board_repository: BoardRepository):
        self.board_repository = board_repository

    async def execute(self, board_id: str, board_data: BoardDTO) -> BoardDTO:
        """
        Update an existing board with the provided data.

        :param board_id: The external ID of the board to update.
        :param board_data: BoardModel containing the updated board details.
        :return: The updated board object.
        """
        to_update = BoardModel(
            name=board_data.name,
            position=board_data.position,
        )

        updated = await self.board_repository.update(board_id, to_update)

        return BoardDTO(
            id=updated.external_id,
            name=updated.name,
            position=updated.position,
            created_at=updated.created_at,
            updated_at=updated.updated_at
        )
